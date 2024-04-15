// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module docprovider-extension
 */
import { PageConfig, URLExt } from '@jupyterlab/coreutils';
import { ServerConnection } from '@jupyterlab/services';
import { INotebookCellExecutor, runCell } from '@jupyterlab/notebook';
export const notebookCellExecutor = {
    id: '@jupyter/docprovider-extension:notebook-cell-executor',
    description: 'Add notebook cell executor that uses REST API instead of kernel protocol over WebSocket.',
    autoStart: true,
    provides: INotebookCellExecutor,
    activate: (app) => {
        if (PageConfig.getOption('serverSideExecution') === 'true') {
            return Object.freeze({ runCell: runCellServerSide });
        }
        return Object.freeze({ runCell });
    }
};
async function runCellServerSide({ cell, notebook, notebookConfig, onCellExecuted, onCellExecutionScheduled, sessionContext, sessionDialogs, translator }) {
    var _a, _b;
    switch (cell.model.type) {
        case 'markdown':
            cell.rendered = true;
            cell.inputHidden = false;
            onCellExecuted({ cell, success: true });
            break;
        case 'code': {
            const kernelId = (_b = (_a = sessionContext === null || sessionContext === void 0 ? void 0 : sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel) === null || _b === void 0 ? void 0 : _b.id;
            const settings = ServerConnection.makeSettings();
            const apiURL = URLExt.join(settings.baseUrl, `api/kernels/${kernelId}/execute`);
            const cellId = cell.model.sharedModel.getId();
            const documentId = `json:notebook:${notebook.sharedModel.getState('file_id')}`;
            const body = `{"cell_id":"${cellId}","document_id":"${documentId}"}`;
            const init = {
                method: 'POST',
                body
            };
            try {
                await ServerConnection.makeRequest(apiURL, init, settings);
            }
            catch (error) {
                throw new ServerConnection.NetworkError(error);
            }
            break;
        }
        default:
            break;
    }
    return Promise.resolve(true);
}
