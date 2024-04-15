/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */
import { ILabShell, IRouter, JupyterFrontEnd } from '@jupyterlab/application';
import { Dialog, showDialog } from '@jupyterlab/apputils';
import { IDefaultFileBrowser, IFileBrowserFactory } from '@jupyterlab/filebrowser';
import { IEditorTracker } from '@jupyterlab/fileeditor';
import { ILoggerRegistry } from '@jupyterlab/logconsole';
import { INotebookTracker } from '@jupyterlab/notebook';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { ITranslator, nullTranslator } from '@jupyterlab/translation';
import { YFile, YNotebook } from '@jupyter/ydoc';
import { ICollaborativeDrive, YDrive } from '@jupyter/docprovider';
/**
 * The command IDs used by the file browser plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.openPath = 'filebrowser:open-path';
})(CommandIDs || (CommandIDs = {}));
/**
 * The default collaborative drive provider.
 */
export const drive = {
    id: '@jupyter/docprovider-extension:drive',
    description: 'The default collaborative drive provider',
    provides: ICollaborativeDrive,
    requires: [ITranslator],
    optional: [],
    activate: (app, translator) => {
        const trans = translator.load('jupyter_collaboration');
        const drive = new YDrive(app.serviceManager.user, trans);
        app.serviceManager.contents.addDrive(drive);
        return drive;
    }
};
/**
 * Plugin to register the shared model factory for the content type 'file'.
 */
export const yfile = {
    id: '@jupyter/docprovider-extension:yfile',
    description: "Plugin to register the shared model factory for the content type 'file'",
    autoStart: true,
    requires: [ICollaborativeDrive],
    optional: [],
    activate: (app, drive) => {
        const yFileFactory = () => {
            return new YFile();
        };
        drive.sharedModelFactory.registerDocumentFactory('file', yFileFactory);
    }
};
/**
 * Plugin to register the shared model factory for the content type 'notebook'.
 */
export const ynotebook = {
    id: '@jupyter/docprovider-extension:ynotebook',
    description: "Plugin to register the shared model factory for the content type 'notebook'",
    autoStart: true,
    requires: [ICollaborativeDrive],
    optional: [ISettingRegistry],
    activate: (app, drive, settingRegistry) => {
        let disableDocumentWideUndoRedo = true;
        // Fetch settings if possible.
        if (settingRegistry) {
            settingRegistry
                .load('@jupyterlab/notebook-extension:tracker')
                .then(settings => {
                const updateSettings = (settings) => {
                    var _a;
                    const enableDocWideUndo = settings === null || settings === void 0 ? void 0 : settings.get('experimentalEnableDocumentWideUndoRedo').composite;
                    disableDocumentWideUndoRedo = (_a = !enableDocWideUndo) !== null && _a !== void 0 ? _a : true;
                };
                updateSettings(settings);
                settings.changed.connect((settings) => updateSettings(settings));
            });
        }
        const yNotebookFactory = () => {
            return new YNotebook({
                disableDocumentWideUndoRedo
            });
        };
        drive.sharedModelFactory.registerDocumentFactory('notebook', yNotebookFactory);
    }
};
/**
 * The default file browser factory provider.
 */
export const defaultFileBrowser = {
    id: '@jupyter/docprovider-extension:defaultFileBrowser',
    description: 'The default file browser factory provider',
    provides: IDefaultFileBrowser,
    requires: [ICollaborativeDrive, IFileBrowserFactory],
    optional: [
        IRouter,
        JupyterFrontEnd.ITreeResolver,
        ILabShell,
        ISettingRegistry
    ],
    activate: async (app, drive, fileBrowserFactory, router, tree, labShell) => {
        const { commands } = app;
        app.serviceManager.contents.addDrive(drive);
        // Manually restore and load the default file browser.
        const defaultBrowser = fileBrowserFactory.createFileBrowser('filebrowser', {
            auto: false,
            restore: false,
            driveName: drive.name
        });
        void Private.restoreBrowser(defaultBrowser, commands, router, tree, labShell);
        return defaultBrowser;
    }
};
/**
 * The default collaborative drive provider.
 */
export const logger = {
    id: '@jupyter/docprovider-extension:logger',
    description: 'A logging plugin for debugging purposes.',
    autoStart: true,
    optional: [ILoggerRegistry, IEditorTracker, INotebookTracker, ITranslator],
    activate: (app, loggerRegistry, fileTracker, nbTracker, translator) => {
        const trans = (translator !== null && translator !== void 0 ? translator : nullTranslator).load('jupyter_collaboration');
        const schemaID = 'https://schema.jupyter.org/jupyter_collaboration/session/v1';
        if (!loggerRegistry) {
            app.serviceManager.events.stream.connect((_, emission) => {
                var _a, _b;
                if (emission.schema_id === schemaID) {
                    console.debug(`[${emission.room}(${emission.path})] ${(_a = emission.action) !== null && _a !== void 0 ? _a : ''}: ${(_b = emission.msg) !== null && _b !== void 0 ? _b : ''}`);
                    if (emission.level === 'WARNING') {
                        showDialog({
                            title: trans.__('Warning'),
                            body: trans.__(`Two collaborative sessions are accessing the file ${emission.path} simultaneously.
                \nOpening the same file using different views simultaneously is not supported. Please, close one view; otherwise, you might lose some of your progress.`),
                            buttons: [Dialog.okButton()]
                        });
                    }
                }
            });
            return;
        }
        const loggers = new Map();
        const addLogger = (sender, document) => {
            const logger = loggerRegistry.getLogger(document.context.path);
            loggers.set(document.context.localPath, logger);
            document.disposed.connect(document => {
                loggers.delete(document.context.localPath);
            });
        };
        if (fileTracker) {
            fileTracker.widgetAdded.connect(addLogger);
        }
        if (nbTracker) {
            nbTracker.widgetAdded.connect(addLogger);
        }
        void (async () => {
            var _a, _b;
            const { events } = app.serviceManager;
            for await (const emission of events.stream) {
                if (emission.schema_id === schemaID) {
                    const logger = loggers.get(emission.path);
                    logger === null || logger === void 0 ? void 0 : logger.log({
                        type: 'text',
                        level: emission.level.toLowerCase(),
                        data: `[${emission.room}] ${(_a = emission.action) !== null && _a !== void 0 ? _a : ''}: ${(_b = emission.msg) !== null && _b !== void 0 ? _b : ''}`
                    });
                    if (emission.level === 'WARNING') {
                        showDialog({
                            title: trans.__('Warning'),
                            body: trans.__(`Two collaborative sessions are accessing the file %1 simultaneously.
                \nOpening a document with multiple views simultaneously is not supported. Please close one view; otherwise, you might lose some of your progress.`, emission.path),
                            buttons: [Dialog.warnButton({ label: trans.__('Ok') })]
                        });
                    }
                }
            }
        })();
    }
};
var Private;
(function (Private) {
    /**
     * Restores file browser state and overrides state if tree resolver resolves.
     */
    async function restoreBrowser(browser, commands, router, tree, labShell) {
        const restoring = 'jp-mod-restoring';
        browser.addClass(restoring);
        if (!router) {
            await browser.model.restore(browser.id);
            await browser.model.refresh();
            browser.removeClass(restoring);
            return;
        }
        const listener = async () => {
            router.routed.disconnect(listener);
            const paths = await (tree === null || tree === void 0 ? void 0 : tree.paths);
            if ((paths === null || paths === void 0 ? void 0 : paths.file) || (paths === null || paths === void 0 ? void 0 : paths.browser)) {
                // Restore the model without populating it.
                await browser.model.restore(browser.id, false);
                if (paths.file) {
                    await commands.execute(CommandIDs.openPath, {
                        path: paths.file,
                        dontShowBrowser: true
                    });
                }
                if (paths.browser) {
                    await commands.execute(CommandIDs.openPath, {
                        path: paths.browser,
                        dontShowBrowser: true
                    });
                }
            }
            else {
                await browser.model.restore(browser.id);
                await browser.model.refresh();
            }
            browser.removeClass(restoring);
            if (labShell === null || labShell === void 0 ? void 0 : labShell.isEmpty('main')) {
                void commands.execute('launcher:create');
            }
        };
        router.routed.connect(listener);
    }
    Private.restoreBrowser = restoreBrowser;
})(Private || (Private = {}));
