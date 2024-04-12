import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

/**
 * Initialization data for the Jupyter-Bridge extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'Jupyter-Bridge:plugin',
  description: 'A JupyterLab extension.',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    console.log('JupyterLab extension Jupyter-Bridge is activated!');
  }
};

export default plugin;
