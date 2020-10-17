// Copyright (c) 2020 {{ cookiecutter.author }}
// Distributed under the terms of the BSD-3-Clause License

import {
  JupyterFrontEndPlugin,
  JupyterFrontEnd,
} from '@jupyterlab/application';

import { PLUGIN_ID } from '.';

function activate(app: JupyterFrontEnd) {
  console.warn(`🚀 ${PLUGIN_ID} is active`, app);
}

/**
 * Initialization data for the jupyterlab_robotmode extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  autoStart: true,
  id: PLUGIN_ID,
  requires: [],
  activate,
};

export default [extension];
