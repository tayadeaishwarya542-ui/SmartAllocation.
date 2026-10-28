import os

BASE_DIR = r"C:\Users\hp\OneDrive\Desktop\content-transformer"
MIRROR_DIR = r"C:\Users\hp\OneDrive\Desktop\New folder\content-transformer"

def save_file(rel_path, content):
    for base in [BASE_DIR, MIRROR_DIR]:
        full_path = os.path.join(base, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Saved: {full_path} ({len(content)} chars)")

PIPELINES_JS = r'''// ================================================================
//  Pipelines Page — Multi-Step Sequential Transformation Engine
// ================================================================

let _pipelineStages = [
  { id: 'stage_1', type: 'grammar', enabled: true, opts: { showDiff: 'no' }, status: 'idle', output: '', error: '' },
  { id: 'stage_2', type: 'tone', enabled: true, opts: { targetTone: 'professional' }, status: 'idle', output: '', error: '' },
  { id: 'stage_3', type: 'summarize', enabled: true, opts: { length: 'short' }, status: 'idle', output: '', error: '' },
  { id: 'stage_4', type: 'convert', enabled: true, opts: { targetFormat: 'bullets' }, status: 'idle', output: '', error: '' }
];

let _isPipelineRunning = false;
let _currentStageIndex = -1;
let _cancelRequested = false;
let _pipelineFinalOutput = '';
let _activeStageViewIndex = -1; // -1 for final, or 0..n for specific stage

function renderPipelinesPage() {
  const provider = API.getProvider();
  const model = API.getModel();

  return `
  <div class="page-view">
    <div class="page-header">
      <div class="page-header-top">
        <div>
          <div class="page-title">Sequential Pipeline Studio <span class="grad-text">✦</span></div>
          <div class="page-desc">Chain multiple transformations sequentially. Output of each stage feeds directly into the next.</div>
        </div>
        <div class="flex gap-2 items-center flex-wrap">
          <div class="badge badge-purple" onclick="App.navigate('settings')" style="cursor:pointer;" title="Configure AI provider">
            <i class="ri-cpu-line"></i> ${provider.toUpperCase()}: ${model}
          </div>
          <button class="btn btn-secondary btn-sm" onclick="PipelinesPage.resetAll()">
            <i class="ri-refresh-line"></i> Reset
          </button>
          <button class="btn btn-secondary btn-sm" onclick="PipelinesPage.loadSampleText()">
            <i class="ri-lightbulb-line"></i> Load Sample Text
          </button>
        </div>
      </div>
    </div>

    <!-- Preset Pipelines Selector -->
    <div class="pipeline-presets-bar">
      <div class="section-title" style="font-size:14px;margin-bottom:8px;">
        <i class="ri-flashlight-line" style="color:#fbbf24"></i> Quick Preset Pipelines:
      </div>
      <div class="presets-row">
        ${PIPELINE_PRESETS.map(p => `
          <button class="preset-chip" onclick="PipelinesPage.loadPreset('${p.id}')" title="${p.desc}">
            <i class="${p.icon}"></i>
            <span>${p.name}</span>
          </button>
        `).join('')}
      </div>
    </div>

    <!-- Pipeline Input Area -->
    <div class="pipeline-input-card">
      <div class="editor-header" style="border:none;padding:0 0 10px 0;">
        <div class="editor-title"><i class="ri-input-cursor-move"></i> Pipeline Initial Content</div>
        <div class="editor-actions">
          <span class="word-count" id="pipelineInputWC">0 words</span>
          <button class="icon-btn" onclick="PipelinesPage.pasteInput()" title="Paste"><i class="ri-clipboard-line"></i></button>
          <button class="icon-btn" onclick="PipelinesPage.clearInput()" title="Clear"><i class="ri-delete-bin-line"></i></button>
        </div>
      </div>
      <textarea class="editor-textarea" id="pipelineInputText" placeholder="Enter or paste the source text that will flow through the pipeline stages..." oninput="PipelinesPage.updateInputWC()" style="min-height:100px;"></textarea>
    </div>

    <!-- Pipeline Stages Builder Canvas -->
    <div class="pipeline-builder-card">
      <div class="pipeline-builder-header">
        <div>
          <div class="builder-title"><i class="ri-flow-chart"></i> Active Pipeline Sequence</div>
          <div class="builder-desc">Stages execute in order from top to bottom. Drag or reorder stages as needed.</div>
        </div>
        <div class="flex gap-2 items-center">
          <button class="btn btn-secondary btn-sm" onclick="PipelinesPage.openAddStageModal()">
            <i class="ri-add-line"></i> Add Stage
          </button>
          ${_isPipelineRunning ? `
            <button class="btn btn-danger btn-sm" onclick="PipelinesPage.cancel()">
              <i class="ri-stop-circle-line"></i> Cancel Pipeline
            </button>
          ` : `
            <button class="btn btn-primary btn-sm" onclick="PipelinesPage.run()" id="btnRunPipeline">
              <i class="ri-play-fill"></i> Execute Entire Pipeline
            </button>
          `}
        </div>
      </div>

      <!-- Stage Cards Sequence List -->
      <div class="pipeline-stages-list" id="pipelineStagesList">
        ${renderStagesListHtml()}
      </div>
    </div>

    <!-- Results Section (Visible after execution or when outputs exist) -->
    <div class="pipeline-results-card" id="pipelineResultsSection" style="${_pipelineFinalOutput ? 'display:block;' : 'display:none;'}">
      <div class="pipeline-results-header">
        <div class="flex items-center gap-2">
          <i class="ri-checkbox-circle-fill" style="color:#34d399;font-size:20px;"></i>
          <span style="font-weight:700;font-size:16px;">Pipeline Results</span>
        </div>
        <div class="flex gap-2 items-center">
          <button class="btn btn-secondary btn-sm" onclick="PipelinesPage.copyOutput()"><i class="ri-file-copy-line"></i> Copy</button>
          <button class="btn btn-secondary btn-sm" onclick="PipelinesPage.downloadOutput()"><i class="ri-download-2-line"></i> Download</button>
          <button class="btn btn-secondary btn-sm" onclick="PipelinesPage.sendToTransform()"><i class="ri-arrow-right-line"></i> Send to Transform</button>
        </div>
      </div>

      <!-- Stage Output Navigation Tabs -->
      <div class="pipeline-output-tabs" id="pipelineOutputTabs">
        ${renderPipelineTabsHtml()}
      </div>

      <div class="pipeline-output-view" id="pipelineActiveOutputView">
        ${renderActiveOutputHtml()}
      </div>
    </div>

    <!-- Add Stage Modal -->
    <div id="addStageModal" class="modal-overlay" style="display:none;">
      <div class="modal-box">
        <div class="modal-header">
          <div class="modal-title">Add Stage to Pipeline</div>
          <button class="icon-btn" onclick="PipelinesPage.closeAddStageModal()"><i class="ri-close-line"></i></button>
        </div>
        <div class="modal-body">
          <div class="form-label" style="margin-bottom:10px;">Select Operation:</div>
          <div class="add-stage-grid">
            ${getTransformationTypes().map(t => `
              <div class="add-stage-option" onclick="PipelinesPage.confirmAddStage('${t.id}')">
                <div class="stage-opt-icon"><i class="${t.icon}"></i></div>
                <div class="stage-opt-info">
                  <div class="stage-opt-name">${t.label}</div>
                  <div class="stage-opt-desc">${t.desc}</div>
                </div>
              </div>
            `).join('')}
          </div>
        </div>
      </div>
    </div>

  </div>`;
}

function renderStagesListHtml() {
  if (_pipelineStages.length === 0) {
    return `
      <div class="empty-stages-box">
        <i class="ri-flow-chart"></i>
        <div>No stages configured in this pipeline.</div>
        <button class="btn btn-secondary btn-sm" onclick="PipelinesPage.openAddStageModal()" style="margin-top:10px;">
          <i class="ri-add-line"></i> Add First Stage
        </button>
      </div>
    `;
  }

  return _pipelineStages.map((stage, idx) => {
    const def = TRANSFORMATIONS[stage.type] || {};
    const statusClasses = {
      idle: 'stage-idle',
      running: 'stage-running',
      completed: 'stage-completed',
      failed: 'stage-failed'
    };
    const statusBadges = {
      idle: `<span class="badge badge-secondary">Pending</span>`,
      running: `<span class="badge badge-amber"><i class="ri-loader-4-line spinner"></i> Running</span>`,
      completed: `<span class="badge badge-green"><i class="ri-check-line"></i> Complete</span>`,
      failed: `<span class="badge badge-red"><i class="ri-error-warning-line"></i> Failed</span>`
    };

    return `
      <div class="pipeline-stage-item ${statusClasses[stage.status]} ${!stage.enabled ? 'stage-disabled' : ''}" id="stage-card-${idx}">
        <div class="stage-item-left">
          <div class="stage-index-badge">${idx + 1}</div>
          <div class="stage-toggle" title="Enable or disable this stage">
            <input type="checkbox" id="stage-chk-${idx}" ${stage.enabled ? 'checked' : ''} onchange="PipelinesPage.toggleStage(${idx})" />
          </div>
          <div class="stage-icon-circle"><i class="${def.icon || 'ri-magic-line'}"></i></div>
          <div class="stage-main-meta">
            <div class="stage-title-row">
              <span class="stage-type-name">${def.label || stage.type}</span>
              ${statusBadges[stage.status]}
              ${stage.output ? `<span class="stage-words-tag">${wordCount(stage.output)} words</span>` : ''}
            </div>
            <div class="stage-desc-row">${def.desc || ''}</div>
          </div>
        </div>

        <!-- Stage Dynamic Option Selectors -->
        <div class="stage-options-inline">
          ${renderStageOptionsInline(stage, idx)}
        </div>

        <!-- Stage Reorder & Actions -->
        <div class="stage-item-actions">
          <button class="icon-btn-sm" onclick="PipelinesPage.moveStage(${idx}, -1)" ${idx === 0 ? 'disabled' : ''} title="Move Up">
            <i class="ri-arrow-up-s-line"></i>
          </button>
          <button class="icon-btn-sm" onclick="PipelinesPage.moveStage(${idx}, 1)" ${idx === _pipelineStages.length - 1 ? 'disabled' : ''} title="Move Down">
            <i class="ri-arrow-down-s-line"></i>
          </button>
          ${stage.status === 'failed' ? `
            <button class="btn btn-warning btn-xs" onclick="PipelinesPage.retryFromStage(${idx})" title="Retry this stage">
              <i class="ri-restart-line"></i> Retry
            </button>
          ` : ''}
          <button class="icon-btn-sm btn-delete" onclick="PipelinesPage.removeStage(${idx})" title="Remove stage">
            <i class="ri-delete-bin-line"></i>
          </button>
        </div>

        ${stage.error ? `
          <div class="stage-error-banner">
            <i class="ri-alert-line"></i> ${escapeHtml(stage.error)}
          </div>
        ` : ''}
      </div>
    `;
  }).join('');
}

function renderStageOptionsInline(stage, stageIdx) {
  const def = TRANSFORMATIONS[stage.type];
  if (!def || !def.extraOptions) return '';

  return def.extraOptions.map(opt => {
    const currentVal = stage.opts[opt.id] || opt.default;
    if (opt.type === 'select') {
      return `
        <select class="form-select form-select-xs" onchange="PipelinesPage.updateStageOpt(${stageIdx}, '${opt.id}', this.value)">
          ${opt.choices.map(c => {
            const val = typeof c === 'object' ? c.value : c;
            const lbl = typeof c === 'object' ? c.label : capitalize(c);
            return `<option value="${val}" ${val === currentVal ? 'selected' : ''}>${lbl}</option>`;
          }).join('')}
        </select>
      `;
    }
    return '';
  }).join('');
}

function renderPipelineTabsHtml() {
  const tabs = [];
  tabs.push(`
    <button class="output-tab ${_activeStageViewIndex === -1 ? 'active' : ''}" onclick="PipelinesPage.switchOutputView(-1)">
      Final Output (${wordCount(_pipelineFinalOutput)} words)
    </button>
  `);

  _pipelineStages.forEach((s, idx) => {
    if (s.output) {
      tabs.push(`
        <button class="output-tab ${_activeStageViewIndex === idx ? 'active' : ''}" onclick="PipelinesPage.switchOutputView(${idx})">
          Stage ${idx + 1}: ${TRANSFORMATIONS[s.type]?.label || s.type}
        </button>
      `);
    }
  });

  return tabs.join('');
}

function renderActiveOutputHtml() {
  let content = '';
  if (_activeStageViewIndex === -1) {
    content = _pipelineFinalOutput || 'No output generated yet.';
  } else {
    const s = _pipelineStages[_activeStageViewIndex];
    content = s ? s.output : '';
  }

  return `<div class="formatted-output-box">${escapeHtml(content).replace(/\n/g, '<br>')}</div>`;
}

// Controller
const PipelinesPage = {
  loadPreset(id) {
    const preset = PIPELINE_PRESETS.find(p => p.id === id);
    if (!preset) return;

    _pipelineStages = preset.stages.map((st, i) => ({
      id: `stage_${Date.now()}_${i}`,
      type: st.type,
      enabled: true,
      opts: { ...st.opts },
      status: 'idle',
      output: '',
      error: ''
    }));

    _pipelineFinalOutput = '';
    _activeStageViewIndex = -1;

    const list = document.getElementById('pipelineStagesList');
    if (list) list.innerHTML = renderStagesListHtml();
    const resSec = document.getElementById('pipelineResultsSection');
    if (resSec) resSec.style.display = 'none';

    Toast.show('info', 'Preset Loaded', `Loaded pipeline "${preset.name}" (${preset.stages.length} stages).`);
  },

  loadSampleText() {
    const sample = "The emergence of modern Generative Artificial Intelligence represents a fundamental inflection point across technical and commercial enterprises. By transforming arbitrary unstructured inputs into deterministic, high-efficiency outputs, automated workflows eliminate cognitive friction and accelerate cross-functional delivery. As development architectures embrace decentralized, privacy-first local computing, real-time pipelines empower organizations to adapt content seamlessly without incurring unsustainable infrastructure overhead.";
    const inp = document.getElementById('pipelineInputText');
    if (inp) {
      inp.value = sample;
      this.updateInputWC();
      Toast.show('info', 'Sample Loaded', 'Pipeline source content populated.');
    }
  },

  updateInputWC() {
    const inp = document.getElementById('pipelineInputText');
    const wcEl = document.getElementById('pipelineInputWC');
    if (inp && wcEl) wcEl.textContent = wordCount(inp.value) + ' words';
  },

  pasteInput() {
    navigator.clipboard?.readText?.().then(text => {
      const inp = document.getElementById('pipelineInputText');
      if (inp) {
        inp.value = text;
        this.updateInputWC();
        Toast.show('info', 'Pasted', 'Clipboard content loaded.');
      }
    }).catch(() => Toast.show('warning', 'Clipboard', 'Paste with Ctrl+V directly.'));
  },

  clearInput() {
    const inp = document.getElementById('pipelineInputText');
    if (inp) {
      inp.value = '';
      this.updateInputWC();
    }
  },

  toggleStage(idx) {
    if (_pipelineStages[idx]) {
      _pipelineStages[idx].enabled = !_pipelineStages[idx].enabled;
      const list = document.getElementById('pipelineStagesList');
      if (list) list.innerHTML = renderStagesListHtml();
    }
  },

  moveStage(idx, dir) {
    const targetIdx = idx + dir;
    if (targetIdx < 0 || targetIdx >= _pipelineStages.length) return;
    const temp = _pipelineStages[idx];
    _pipelineStages[idx] = _pipelineStages[targetIdx];
    _pipelineStages[targetIdx] = temp;
    const list = document.getElementById('pipelineStagesList');
    if (list) list.innerHTML = renderStagesListHtml();
  },

  removeStage(idx) {
    _pipelineStages.splice(idx, 1);
    const list = document.getElementById('pipelineStagesList');
    if (list) list.innerHTML = renderStagesListHtml();
  },

  updateStageOpt(idx, key, val) {
    if (_pipelineStages[idx]) {
      _pipelineStages[idx].opts[key] = val;
    }
  },

  openAddStageModal() {
    const m = document.getElementById('addStageModal');
    if (m) m.style.display = 'flex';
  },

  closeAddStageModal() {
    const m = document.getElementById('addStageModal');
    if (m) m.style.display = 'none';
  },

  confirmAddStage(typeId) {
    const def = TRANSFORMATIONS[typeId];
    if (!def) return;

    const defaultOpts = {};
    if (def.extraOptions) {
      def.extraOptions.forEach(o => { defaultOpts[o.id] = o.default; });
    }

    _pipelineStages.push({
      id: `stage_${Date.now()}`,
      type: typeId,
      enabled: true,
      opts: defaultOpts,
      status: 'idle',
      output: '',
      error: ''
    });

    this.closeAddStageModal();
    const list = document.getElementById('pipelineStagesList');
    if (list) list.innerHTML = renderStagesListHtml();
    Toast.show('success', 'Stage Added', `Added ${def.label} to pipeline.`);
  },

  resetAll() {
    _isPipelineRunning = false;
    _cancelRequested = false;
    _currentStageIndex = -1;
    _pipelineFinalOutput = '';
    _activeStageViewIndex = -1;
    _pipelineStages.forEach(s => {
      s.status = 'idle';
      s.output = '';
      s.error = '';
    });
    const list = document.getElementById('pipelineStagesList');
    if (list) list.innerHTML = renderStagesListHtml();
    const resSec = document.getElementById('pipelineResultsSection');
    if (resSec) resSec.style.display = 'none';
  },

  cancel() {
    _cancelRequested = true;
    _isPipelineRunning = false;
    Toast.show('warning', 'Pipeline Canceled', 'Execution halted by user.');
    const list = document.getElementById('pipelineStagesList');
    if (list) list.innerHTML = renderStagesListHtml();
  },

  // Execute entire pipeline sequentially
  async run() {
    const inp = document.getElementById('pipelineInputText')?.value?.trim();
    if (!inp) {
      Toast.show('warning', 'Missing Content', 'Please provide initial text in the Pipeline Initial Content area.');
      document.getElementById('pipelineInputText')?.focus();
      return;
    }

    const enabledStages = _pipelineStages.filter(s => s.enabled);
    if (enabledStages.length === 0) {
      Toast.show('warning', 'No Active Stages', 'Please enable at least one stage in the pipeline sequence.');
      return;
    }

    _isPipelineRunning = true;
    _cancelRequested = false;
    _pipelineFinalOutput = '';
    _activeStageViewIndex = -1;

    // Reset statuses
    _pipelineStages.forEach(s => {
      if (s.enabled) {
        s.status = 'idle';
        s.output = '';
        s.error = '';
      }
    });

    let currentPayload = inp;

    for (let i = 0; i < _pipelineStages.length; i++) {
      const stage = _pipelineStages[i];
      if (!stage.enabled) continue;

      if (_cancelRequested) {
        stage.status = 'idle';
        break;
      }

      _currentStageIndex = i;
      stage.status = 'running';
      this._updateUIStages();

      try {
        const result = await API.executeTransform({
          type: stage.type,
          input: currentPayload,
          opts: stage.opts
        });

        const outputText = typeof result === 'string' ? result : (result.output || '');
        stage.output = outputText;
        stage.status = 'completed';
        stage.error = '';

        // Pass actual output of this stage into next stage!
        currentPayload = outputText;
      } catch (err) {
        stage.status = 'failed';
        stage.error = err.message;
        _isPipelineRunning = false;
        this._updateUIStages();
        Toast.show('error', `Stage ${i + 1} Failed`, `${TRANSFORMATIONS[stage.type]?.label}: ${err.message}`);
        return;
      }
    }

    _isPipelineRunning = false;
    _pipelineFinalOutput = currentPayload;
    this._updateUIStages();
    this._showResults();

    // Persist to history
    AppState.addHistory({
      type: 'pipeline',
      opts: { stageCount: enabledStages.length },
      input: inp,
      output: _pipelineFinalOutput,
      provider: API.getProvider(),
      model: API.getModel(),
      timestamp: Date.now()
    });

    Toast.show('success', 'Pipeline Finished', 'All pipeline stages executed successfully!');
  },

  // Retry from specific failed stage
  async retryFromStage(startIndex) {
    const initialText = document.getElementById('pipelineInputText')?.value?.trim();
    if (!initialText) return;

    // Find input payload for this stage
    let payload = initialText;
    for (let j = startIndex - 1; j >= 0; j--) {
      if (_pipelineStages[j].enabled && _pipelineStages[j].output) {
        payload = _pipelineStages[j].output;
        break;
      }
    }

    _isPipelineRunning = true;
    _cancelRequested = false;

    for (let i = startIndex; i < _pipelineStages.length; i++) {
      const stage = _pipelineStages[i];
      if (!stage.enabled) continue;
      if (_cancelRequested) break;

      stage.status = 'running';
      this._updateUIStages();

      try {
        const result = await API.executeTransform({
          type: stage.type,
          input: payload,
          opts: stage.opts
        });
        const out = typeof result === 'string' ? result : (result.output || '');
        stage.output = out;
        stage.status = 'completed';
        stage.error = '';
        payload = out;
      } catch (err) {
        stage.status = 'failed';
        stage.error = err.message;
        _isPipelineRunning = false;
        this._updateUIStages();
        Toast.show('error', `Stage ${i + 1} Failed`, err.message);
        return;
      }
    }

    _isPipelineRunning = false;
    _pipelineFinalOutput = payload;
    this._updateUIStages();
    this._showResults();
    Toast.show('success', 'Pipeline Resumed', 'Subsequent pipeline stages completed successfully.');
  },

  _updateUIStages() {
    const list = document.getElementById('pipelineStagesList');
    if (list) list.innerHTML = renderStagesListHtml();
  },

  _showResults() {
    const sec = document.getElementById('pipelineResultsSection');
    const tabs = document.getElementById('pipelineOutputTabs');
    const view = document.getElementById('pipelineActiveOutputView');

    if (sec) sec.style.display = 'block';
    if (tabs) tabs.innerHTML = renderPipelineTabsHtml();
    if (view) view.innerHTML = renderActiveOutputHtml();

    sec?.scrollIntoView({ behavior: 'smooth' });
  },

  switchOutputView(stageIndex) {
    _activeStageViewIndex = stageIndex;
    const tabs = document.getElementById('pipelineOutputTabs');
    const view = document.getElementById('pipelineActiveOutputView');
    if (tabs) tabs.innerHTML = renderPipelineTabsHtml();
    if (view) view.innerHTML = renderActiveOutputHtml();
  },

  async copyOutput() {
    const text = _activeStageViewIndex === -1 ? _pipelineFinalOutput : (_pipelineStages[_activeStageViewIndex]?.output || '');
    if (!text) return;
    try {
      await navigator.clipboard.writeText(text);
      Toast.show('success', 'Copied!', 'Pipeline output copied to clipboard.');
    } catch {
      Toast.show('error', 'Copy Failed', 'Unable to write to clipboard.');
    }
  },

  downloadOutput() {
    const text = _activeStageViewIndex === -1 ? _pipelineFinalOutput : (_pipelineStages[_activeStageViewIndex]?.output || '');
    if (!text) return;
    const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `transformai-pipeline-${Date.now()}.txt`;
    a.click();
    Toast.show('success', 'Downloaded', 'Pipeline result saved as .txt file.');
  },

  sendToTransform() {
    if (!_pipelineFinalOutput) return;
    App.navigate('transform');
    setTimeout(() => {
      const inp = document.getElementById('inputContent');
      if (inp) {
        inp.value = _pipelineFinalOutput;
        TransformPage.updateWordCount();
        Toast.show('info', 'Loaded in Transform', 'Pipeline final output loaded into Transform input.');
      }
    }, 250);
  }
};
'''

save_file("pages/pipelines.js", PIPELINES_JS)
