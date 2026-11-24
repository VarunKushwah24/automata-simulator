/**
 * Automata Theory Simulator - Frontend Engine
 * Topic 14: Mealy <-> Moore Conversion
 * CSET302 Automata Theory and Computability - Milestone II
 */

// Application State
const state = {
  mode: 'MealyToMoore', // or 'MooreToMealy'
  presets: {},
  sourceMachine: null,
  convertedMachine: null,
  conversionReport: null,
  activeSourcePresetId: 'mealy_seq_101',
  
  // Simulation State
  simSourceResult: null,
  simConvertedResult: null,
  currentSimStep: 0,
  isPlaying: false,
  playTimer: null,
  playSpeedMs: 900
};

// DOM Elements
const elements = {
  toggleMooreToMealy: document.getElementById('toggleMooreToMealy'),
  toggleMealyToMoore: document.getElementById('toggleMealyToMoore'),
  presetSelect: document.getElementById('presetSelect'),
  btnLoadPreset: document.getElementById('btnLoadPreset'),
  btnNewCustom: document.getElementById('btnNewCustom'),
  btnUploadImage: document.getElementById('btnUploadImage'),
  btnPasteScreenshot: document.getElementById('btnPasteScreenshot'),
  imageFileInput: document.getElementById('imageFileInput'),
  pasteDropZone: document.getElementById('pasteDropZone'),
  btnExportJson: document.getElementById('btnExportJson'),
  btnImportJson: document.getElementById('btnImportJson'),
  importFileInput: document.getElementById('importFileInput'),
  btnConvert: document.getElementById('btnConvert'),
  defaultStartOutputInput: document.getElementById('defaultStartOutput'),
  startOutputContainer: document.getElementById('startOutputContainer'),
  
  // Machine Panels
  sourceTitle: document.getElementById('sourceTitle'),
  sourceTuple: document.getElementById('sourceTuple'),
  sourceSvg: document.getElementById('sourceSvg'),
  sourceTable: document.getElementById('sourceTable'),
  
  convertedTitle: document.getElementById('convertedTitle'),
  convertedTuple: document.getElementById('convertedTuple'),
  convertedSvg: document.getElementById('convertedSvg'),
  convertedTable: document.getElementById('convertedTable'),
  
  // Step walkthrough
  stepsContainer: document.getElementById('stepsContainer'),
  conversionSummary: document.getElementById('conversionSummary'),
  
  // Simulation
  inputString: document.getElementById('inputString'),
  btnSimulate: document.getElementById('btnSimulate'),
  btnStepBack: document.getElementById('btnStepBack'),
  btnStepForward: document.getElementById('btnStepForward'),
  btnPlayPause: document.getElementById('btnPlayPause'),
  btnResetSim: document.getElementById('btnResetSim'),
  simSpeedRange: document.getElementById('simSpeedRange'),
  inputTapeCells: document.getElementById('inputTapeCells'),
  sourceTapeCells: document.getElementById('sourceTapeCells'),
  convertedTapeCells: document.getElementById('convertedTapeCells'),
  simLogBox: document.getElementById('simLogBox'),
  
  // Verification
  verificationTableBody: document.getElementById('verificationTableBody'),
  btnRunAllTests: document.getElementById('btnRunAllTests'),
  
  // Image Upload Modal
  imageOcrModal: document.getElementById('imageOcrModal'),
  btnCloseImageModal: document.getElementById('btnCloseImageModal'),
  btnCancelImageModal: document.getElementById('btnCancelImageModal'),
  btnApplyImageConversion: document.getElementById('btnApplyImageConversion'),
  imageOcrLoading: document.getElementById('imageOcrLoading'),
  imageOcrResultContent: document.getElementById('imageOcrResultContent'),
  ocrDetectedBadge: document.getElementById('ocrDetectedBadge'),
  ocrSummaryText: document.getElementById('ocrSummaryText'),
  ocrRawLines: document.getElementById('ocrRawLines'),
  ocrMachineOverview: document.getElementById('ocrMachineOverview'),
  
  // Visual Diagram Studio Elements
  btnDrawDiagram: document.getElementById('btnDrawDiagram'),
  btnEditCurrentDiagram: document.getElementById('btnEditCurrentDiagram'),
  diagramStudioModal: document.getElementById('diagramStudioModal'),
  btnCloseStudioModal: document.getElementById('btnCloseStudioModal'),
  btnCancelStudio: document.getElementById('btnCancelStudio'),
  btnApplyStudioMachine: document.getElementById('btnApplyStudioMachine'),
  studioMachineType: document.getElementById('studioMachineType'),
  toolSelect: document.getElementById('toolSelect'),
  toolAddState: document.getElementById('toolAddState'),
  toolAddTransition: document.getElementById('toolAddTransition'),
  toolDelete: document.getElementById('toolDelete'),
  btnStudioResetCircle: document.getElementById('btnStudioResetCircle'),
  btnStudioClear: document.getElementById('btnStudioClear'),
  studioCanvasWrapper: document.getElementById('studioCanvasWrapper'),
  studioSvg: document.getElementById('studioSvg'),
  studioCanvasHint: document.getElementById('studioCanvasHint'),
  studioNodeInspector: document.getElementById('studioNodeInspector'),
  studioLiveTable: document.getElementById('studioLiveTable'),
  
  // Transition Prompt Elements
  transitionPromptModal: document.getElementById('transitionPromptModal'),
  transPromptTitle: document.getElementById('transPromptTitle'),
  promptInputSymbol: document.getElementById('promptInputSymbol'),
  promptOutputContainer: document.getElementById('promptOutputContainer'),
  promptOutputSymbol: document.getElementById('promptOutputSymbol'),
  btnCancelTransitionPrompt: document.getElementById('btnCancelTransitionPrompt'),
  btnConfirmTransitionPrompt: document.getElementById('btnConfirmTransitionPrompt'),

  // Modal
  customModal: document.getElementById('customModal'),
  btnCloseModal: document.getElementById('btnCloseModal'),
  btnCancelModal: document.getElementById('btnCancelModal'),
  btnSaveCustomMachine: document.getElementById('btnSaveCustomMachine'),
  customMachineType: document.getElementById('customMachineType'),
  customMachineName: document.getElementById('customMachineName'),
  customStates: document.getElementById('customStates'),
  customAlphabet: document.getElementById('customAlphabet'),
  customOutputs: document.getElementById('customOutputs'),
  customStartState: document.getElementById('customStartState'),
  customDefinitionArea: document.getElementById('customDefinitionArea'),
  customValidationMsg: document.getElementById('customValidationMsg')
};

// Initialize Application
document.addEventListener('DOMContentLoaded', async () => {
  setupEventListeners();
  await loadPresets();
  setMode('MealyToMoore');
});

function setupEventListeners() {
  // Mode toggles
  elements.toggleMooreToMealy.addEventListener('click', () => setMode('MooreToMealy'));
  elements.toggleMealyToMoore.addEventListener('click', () => setMode('MealyToMoore'));
  
  // Presets & actions
  elements.btnLoadPreset.addEventListener('click', loadSelectedPreset);
  elements.presetSelect.addEventListener('change', loadSelectedPreset);
  elements.btnConvert.addEventListener('click', runConversion);
  
  // Export / Import
  elements.btnExportJson.addEventListener('click', exportMachineJson);
  elements.btnImportJson.addEventListener('click', () => elements.importFileInput.click());
  elements.importFileInput.addEventListener('change', handleImportJson);

  // Image Upload & Paste
  elements.btnUploadImage.addEventListener('click', () => elements.imageFileInput.click());
  elements.imageFileInput.addEventListener('change', handleImageUpload);
  elements.btnPasteScreenshot.addEventListener('click', handlePasteButtonClick);
  elements.pasteDropZone.addEventListener('click', () => elements.imageFileInput.click());
  
  // Drag and drop support on dropzone
  elements.pasteDropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    elements.pasteDropZone.style.borderColor = 'var(--success)';
  });
  elements.pasteDropZone.addEventListener('dragleave', (e) => {
    e.preventDefault();
    elements.pasteDropZone.style.borderColor = 'var(--primary)';
  });
  elements.pasteDropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    elements.pasteDropZone.style.borderColor = 'var(--primary)';
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      processImageBlob(e.dataTransfer.files[0]);
    }
  });

  // Global Ctrl+V Screenshot Paste Listener
  window.addEventListener('paste', handleGlobalPaste);

  elements.btnCloseImageModal.addEventListener('click', () => elements.imageOcrModal.classList.remove('active'));
  elements.btnCancelImageModal.addEventListener('click', () => elements.imageOcrModal.classList.remove('active'));
  elements.btnApplyImageConversion.addEventListener('click', applyImageConversion);
  
  // Tabs
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      const tabId = btn.getAttribute('data-tab');
      document.getElementById(tabId).classList.add('active');
    });
  });
  
  // Quick test string pills
  document.querySelectorAll('.test-pill').forEach(pill => {
    pill.addEventListener('click', () => {
      elements.inputString.value = pill.textContent.trim();
      startSimulation();
    });
  });
  
  // Simulation controls
  elements.btnSimulate.addEventListener('click', startSimulation);
  elements.btnResetSim.addEventListener('click', resetSimulation);
  elements.btnStepForward.addEventListener('click', stepForward);
  elements.btnStepBack.addEventListener('click', stepBack);
  elements.btnPlayPause.addEventListener('click', togglePlayPause);
  elements.simSpeedRange.addEventListener('input', (e) => {
    state.playSpeedMs = 1500 - parseInt(e.target.value);
    if (state.isPlaying) {
      clearInterval(state.playTimer);
      state.playTimer = setInterval(stepForward, state.playSpeedMs);
    }
  });
  
  // Verification
  elements.btnRunAllTests.addEventListener('click', runAllVerificationTests);

  // Visual Diagram Studio Actions
  elements.btnDrawDiagram.addEventListener('click', openDiagramStudioNew);
  elements.btnEditCurrentDiagram.addEventListener('click', openDiagramStudioEditCurrent);
  elements.btnCloseStudioModal.addEventListener('click', closeDiagramStudio);
  elements.btnCancelStudio.addEventListener('click', closeDiagramStudio);
  elements.studioMachineType.addEventListener('change', handleStudioTypeChange);
  
  elements.toolSelect.addEventListener('click', () => setStudioTool('select'));
  elements.toolAddState.addEventListener('click', () => setStudioTool('addState'));
  elements.toolAddTransition.addEventListener('click', () => setStudioTool('addTransition'));
  elements.toolDelete.addEventListener('click', () => setStudioTool('delete'));
  elements.btnStudioResetCircle.addEventListener('click', studioAutoArrange);
  elements.btnStudioClear.addEventListener('click', studioClearCanvas);
  elements.btnApplyStudioMachine.addEventListener('click', applyStudioDiagram);
  
  // Transition prompt
  elements.btnCancelTransitionPrompt.addEventListener('click', closeTransitionPrompt);
  elements.btnConfirmTransitionPrompt.addEventListener('click', confirmTransitionPrompt);
  
  // Studio SVG Interaction
  elements.studioSvg.addEventListener('mousedown', handleStudioCanvasMouseDown);
  window.addEventListener('mousemove', handleStudioCanvasMouseMove);
  window.addEventListener('mouseup', handleStudioCanvasMouseUp);
  elements.studioSvg.addEventListener('click', handleStudioCanvasClick);
  
  // Modal Custom Builder
  elements.btnNewCustom.addEventListener('click', openCustomModal);
  elements.btnCloseModal.addEventListener('click', closeCustomModal);
  elements.btnCancelModal.addEventListener('click', closeCustomModal);
  elements.btnSaveCustomMachine.addEventListener('click', saveCustomMachine);
  elements.customMachineType.addEventListener('change', updateCustomFieldsPlaceholder);
}

// Set Conversion Mode
function setMode(newMode, shouldLoadPreset = true) {
  state.mode = newMode;
  if (newMode === 'MooreToMealy') {
    elements.toggleMooreToMealy.classList.add('active');
    elements.toggleMealyToMoore.classList.remove('active');
    elements.startOutputContainer.style.display = 'none';
    elements.btnConvert.innerHTML = `Convert Moore → Mealy <span style="font-size:1.1rem">➔</span>`;
  } else {
    elements.toggleMealyToMoore.classList.add('active');
    elements.toggleMooreToMealy.classList.remove('active');
    elements.startOutputContainer.style.display = 'flex';
    elements.btnConvert.innerHTML = `Convert Mealy → Moore <span style="font-size:1.1rem">➔</span>`;
  }
  updatePresetDropdown();
  if (shouldLoadPreset) {
    loadSelectedPreset();
  }
}

// Fetch Presets from Server
async function loadPresets() {
  try {
    const res = await fetch('/api/presets');
    state.presets = await res.json();
    updatePresetDropdown();
  } catch (err) {
    console.error("Error loading presets:", err);
  }
}

function updatePresetDropdown() {
  elements.presetSelect.innerHTML = '';
  const targetType = state.mode === 'MooreToMealy' ? 'Moore' : 'Mealy';
  
  for (const [id, preset] of Object.entries(state.presets)) {
    if (preset.type === targetType) {
      const opt = document.createElement('option');
      opt.value = id;
      opt.textContent = `${preset.name} (${preset.type})`;
      elements.presetSelect.appendChild(opt);
    }
  }
  if (elements.presetSelect.options.length > 0) {
    elements.presetSelect.selectedIndex = 0;
  }
}

function loadSelectedPreset() {
  const selectedId = elements.presetSelect.value;
  if (!selectedId || !state.presets[selectedId]) return;
  
  const preset = state.presets[selectedId];
  state.sourceMachine = JSON.parse(JSON.stringify(preset.data));
  state.sourceMachine.type = preset.type;
  state.convertedMachine = null;
  state.conversionReport = null;
  
  renderSourceMachine();
  clearConvertedMachine();
  clearSimulation();
  clearSteps();
  
  // Auto-run conversion for seamless experience
  runConversion();
}

// Render Source Machine
function renderSourceMachine() {
  const m = state.sourceMachine;
  if (!m) return;
  
  elements.sourceTitle.innerHTML = `
    <span>${m.name || 'Source Automaton'}</span>
    <span class="badge ${m.type === 'Moore' ? 'badge-primary' : 'badge-accent'}">${m.type}</span>
  `;
  
  elements.sourceTuple.innerHTML = `
    <span><strong>Q:</strong> {${m.states.join(', ')}}</span>
    <span><strong>Σ:</strong> {${m.input_alphabet.join(', ')}}</span>
    <span><strong>Δ:</strong> {${m.output_alphabet.join(', ')}}</span>
    <span><strong>q₀:</strong> ${m.start_state}</span>
  `;
  
  renderTable(elements.sourceTable, m);
  renderSvgGraph(elements.sourceSvg, m);
}

// Clear Converted Machine
function clearConvertedMachine() {
  elements.convertedTitle.innerHTML = `<span>Target Machine</span><span class="badge badge-outline">Pending</span>`;
  elements.convertedTuple.innerHTML = `<span>Click "Convert" to generate equivalent machine.</span>`;
  elements.convertedTable.innerHTML = `<p style="padding:1rem; color:var(--text-muted); text-align:center;">Conversion not yet executed.</p>`;
  elements.convertedSvg.innerHTML = `
    <text x="50%" y="50%" text-anchor="middle" dominant-baseline="middle" fill="#94a3b8" font-size="14">
      Converted state diagram will appear here
    </text>
  `;
}

// Run Conversion
async function runConversion() {
  if (!state.sourceMachine) return;
  
  const startOut = elements.defaultStartOutputInput.value.trim() || "0";
  try {
    const payload = {
      machine_type: state.sourceMachine.type,
      machine_data: state.sourceMachine,
      default_start_output: startOut,
      target_name: `${state.sourceMachine.name} (Converted)`
    };
    
    const res = await fetch('/api/convert', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    
    if (!res.ok) {
      const err = await res.json();
      alert(`Conversion Error: ${err.detail || 'Failed to convert'}`);
      return;
    }
    
    const data = await res.json();
    state.convertedMachine = data.converted;
    state.conversionReport = data;
    
    renderConvertedMachine();
    renderConversionSteps(data.steps, data.summary, data.equivalence_verified);
    renderVerificationTable(data.test_results);
    
    // Reset simulation
    startSimulation();
  } catch (err) {
    console.error("Conversion failed:", err);
    alert(`Error: ${err.message}`);
  }
}

// Render Converted Machine
function renderConvertedMachine() {
  const m = state.convertedMachine;
  if (!m) return;
  
  elements.convertedTitle.innerHTML = `
    <span>${m.name}</span>
    <span class="badge ${m.type === 'Moore' ? 'badge-primary' : 'badge-accent'}">${m.type}</span>
  `;
  
  elements.convertedTuple.innerHTML = `
    <span><strong>Q':</strong> {${m.states.join(', ')}}</span>
    <span><strong>Σ:</strong> {${m.input_alphabet.join(', ')}}</span>
    <span><strong>Δ:</strong> {${m.output_alphabet.join(', ')}}</span>
    <span><strong>q'₀:</strong> ${m.start_state}</span>
  `;
  
  renderTable(elements.convertedTable, m);
  renderSvgGraph(elements.convertedSvg, m);
}

// Render Transition Table
function renderTable(container, m) {
  let html = `<table class="data-table"><thead><tr>`;
  html += `<th>Present State</th>`;
  
  if (m.type === 'Moore') {
    html += `<th>Output λ(q)</th>`;
    m.input_alphabet.forEach(a => {
      html += `<th>Next State (a = '${a}')</th>`;
    });
  } else {
    m.input_alphabet.forEach(a => {
      html += `<th>Input '${a}' (Next, Out)</th>`;
    });
  }
  html += `</tr></thead><tbody>`;
  
  // Build lookup
  const transMap = {};
  m.transitions.forEach(t => {
    transMap[`${t.from},${t.symbol}`] = t;
  });
  
  m.states.forEach(q => {
    const isStart = (q === m.start_state);
    html += `<tr class="${isStart ? 'start-state-row' : ''}">`;
    html += `<td class="state-col">${q}</td>`;
    
    if (m.type === 'Moore') {
      const out = m.state_outputs ? m.state_outputs[q] : '-';
      html += `<td><strong>${out}</strong></td>`;
      m.input_alphabet.forEach(a => {
        const t = transMap[`${q},${a}`];
        html += `<td>${t ? t.to : '-'}</td>`;
      });
    } else {
      m.input_alphabet.forEach(a => {
        const t = transMap[`${q},${a}`];
        if (t) {
          html += `<td>(${t.to}, <strong>${t.output}</strong>)</td>`;
        } else {
          html += `<td>-</td>`;
        }
      });
    }
    html += `</tr>`;
  });
  
  html += `</tbody></table>`;
  container.innerHTML = html;
}

// Standalone SVG Graph Renderer
function renderSvgGraph(svg, m, activeState = null, activeTransition = null) {
  svg.innerHTML = '';
  if (!m || !m.states || m.states.length === 0) return;
  
  const width = svg.clientWidth || 500;
  const height = svg.clientHeight || 380;
  svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
  
  const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
  defs.innerHTML = `
    <marker id="arrow" viewBox="0 0 10 10" refX="24" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#475569" />
    </marker>
    <marker id="arrow-active" viewBox="0 0 10 10" refX="24" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#2563eb" />
    </marker>
  `;
  svg.appendChild(defs);
  
  // Arrange nodes in circle
  const centerX = width / 2;
  const centerY = height / 2;
  const radius = Math.min(centerX, centerY) - 60;
  const n = m.states.length;
  const nodePositions = {};
  
  m.states.forEach((stateName, idx) => {
    const angle = (2 * Math.PI * idx) / n - Math.PI / 2;
    nodePositions[stateName] = {
      x: centerX + radius * Math.cos(angle),
      y: centerY + radius * Math.sin(angle)
    };
  });
  
  // Group transitions by pair (from, to) to aggregate labels
  const edgeGroups = {};
  m.transitions.forEach(t => {
    const key = `${t.from}->${t.to}`;
    if (!edgeGroups[key]) edgeGroups[key] = [];
    edgeGroups[key].push(t);
  });
  
  const edgesG = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  svg.appendChild(edgesG);
  
  // Draw transitions
  for (const [key, tList] of Object.entries(edgeGroups)) {
    const [fromNode, toNode] = key.split('->');
    const p1 = nodePositions[fromNode];
    const p2 = nodePositions[toNode];
    if (!p1 || !p2) continue;
    
    // Label
    let label = '';
    if (m.type === 'Moore') {
      label = tList.map(t => t.symbol).join(', ');
    } else {
      label = tList.map(t => `${t.symbol}/${t.output}`).join(', ');
    }

    const isEdgeActive = Boolean(
      activeTransition &&
      activeTransition.from === fromNode &&
      activeTransition.to === toNode
    );
    
    if (fromNode === toNode) {
      // Self loop
      const loopRadius = 24;
      const angle = Math.atan2(p1.y - centerY, p1.x - centerX);
      const loopCenterX = p1.x + 35 * Math.cos(angle);
      const loopCenterY = p1.y + 35 * Math.sin(angle);
      
      const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      const startAngle = angle - 0.7;
      const endAngle = angle + 0.7;
      const x1 = p1.x + 22 * Math.cos(startAngle);
      const y1 = p1.y + 22 * Math.sin(startAngle);
      const x2 = p1.x + 22 * Math.cos(endAngle);
      const y2 = p1.y + 22 * Math.sin(endAngle);
      
      path.setAttribute('d', `M ${x1} ${y1} C ${loopCenterX - 15} ${loopCenterY - 15}, ${loopCenterX + 15} ${loopCenterY + 15}, ${x2} ${y2}`);
      path.setAttribute('fill', 'none');
      path.setAttribute('stroke', isEdgeActive ? '#2563eb' : '#64748b');
      path.setAttribute('stroke-width', isEdgeActive ? '3.5' : '2');
      path.setAttribute('marker-end', isEdgeActive ? 'url(#arrow-active)' : 'url(#arrow)');
      if (isEdgeActive) {
        path.setAttribute('filter', 'drop-shadow(0 0 5px rgba(37,99,235,0.5))');
      }
      edgesG.appendChild(path);
      
      // Label text
      const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      text.setAttribute('x', loopCenterX);
      text.setAttribute('y', loopCenterY - 4);
      text.setAttribute('text-anchor', 'middle');
      text.setAttribute('fill', isEdgeActive ? '#1d4ed8' : '#0f172a');
      text.setAttribute('font-size', '11');
      text.setAttribute('font-weight', '700');
      text.textContent = label;
      edgesG.appendChild(text);
    } else {
      // Curved edge between two nodes
      const dx = p2.x - p1.x;
      const dy = p2.y - p1.y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      
      // Calculate curve control point
      const curvature = 24;
      const nx = -dy / dist;
      const ny = dx / dist;
      const cx = (p1.x + p2.x) / 2 + nx * curvature;
      const cy = (p1.y + p2.y) / 2 + ny * curvature;
      
      const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      path.setAttribute('d', `M ${p1.x} ${p1.y} Q ${cx} ${cy} ${p2.x} ${p2.y}`);
      path.setAttribute('fill', 'none');
      path.setAttribute('stroke', isEdgeActive ? '#2563eb' : '#64748b');
      path.setAttribute('stroke-width', isEdgeActive ? '3.5' : '2');
      path.setAttribute('marker-end', isEdgeActive ? 'url(#arrow-active)' : 'url(#arrow)');
      if (isEdgeActive) {
        path.setAttribute('filter', 'drop-shadow(0 0 5px rgba(37,99,235,0.5))');
      }
      edgesG.appendChild(path);
      
      // Label with background pill
      const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      text.setAttribute('x', cx);
      text.setAttribute('y', cy);
      text.setAttribute('text-anchor', 'middle');
      text.setAttribute('fill', isEdgeActive ? '#1d4ed8' : '#1e293b');
      text.setAttribute('font-size', '11');
      text.setAttribute('font-weight', '700');
      text.setAttribute('paint-order', 'stroke');
      text.setAttribute('stroke', '#ffffff');
      text.setAttribute('stroke-width', '4');
      text.textContent = label;
      edgesG.appendChild(text);
    }
  }
  
  // Draw nodes
  const nodesG = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  svg.appendChild(nodesG);
  
  m.states.forEach(stateName => {
    const pos = nodePositions[stateName];
    const isStart = (stateName === m.start_state);
    const isActive = (stateName === activeState);
    
    const nodeG = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    
    // Start state indicator arrow
    if (isStart) {
      const startArrow = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      startArrow.setAttribute('d', `M ${pos.x - 45} ${pos.y} L ${pos.x - 24} ${pos.y}`);
      startArrow.setAttribute('stroke', '#2563eb');
      startArrow.setAttribute('stroke-width', '3');
      startArrow.setAttribute('marker-end', 'url(#arrow-active)');
      nodeG.appendChild(startArrow);
      
      const startText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      startText.setAttribute('x', pos.x - 48);
      startText.setAttribute('y', pos.y + 4);
      startText.setAttribute('text-anchor', 'end');
      startText.setAttribute('fill', '#2563eb');
      startText.setAttribute('font-size', '10');
      startText.setAttribute('font-weight', '700');
      startText.textContent = 'Start';
      nodeG.appendChild(startText);
    }
    
    // Circle
    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle.setAttribute('cx', pos.x);
    circle.setAttribute('cy', pos.y);
    circle.setAttribute('r', '22');
    circle.setAttribute('fill', isActive ? '#dbeafe' : '#ffffff');
    circle.setAttribute('stroke', isActive ? '#2563eb' : (isStart ? '#3b82f6' : '#475569'));
    circle.setAttribute('stroke-width', isActive ? '3.5' : (isStart ? '2.5' : '2'));
    if (isActive) {
      circle.setAttribute('filter', 'drop-shadow(0 0 6px rgba(37,99,235,0.4))');
    }
    nodeG.appendChild(circle);
    
    // State Name
    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('x', pos.x);
    text.setAttribute('y', m.type === 'Moore' ? pos.y - 2 : pos.y + 4);
    text.setAttribute('text-anchor', 'middle');
    text.setAttribute('fill', '#0f172a');
    text.setAttribute('font-size', '12');
    text.setAttribute('font-weight', '700');
    text.textContent = stateName;
    nodeG.appendChild(text);
    
    // For Moore Machine: Display State Output inside or just below the circle
    if (m.type === 'Moore' && m.state_outputs) {
      const outText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      outText.setAttribute('x', pos.x);
      outText.setAttribute('y', pos.y + 12);
      outText.setAttribute('text-anchor', 'middle');
      outText.setAttribute('fill', '#dc2626');
      outText.setAttribute('font-size', '10');
      outText.setAttribute('font-weight', '700');
      outText.textContent = `/${m.state_outputs[stateName] || '?'}`;
      nodeG.appendChild(outText);
    }
    
    nodesG.appendChild(nodeG);
  });
}

// Render Step-by-Step Conversion Walkthrough
function renderConversionSteps(steps, summary, isEq) {
  elements.conversionSummary.innerHTML = `
    <div style="padding:0.75rem 1rem; background:${isEq ? '#ecfdf5' : '#fffbeb'}; border-left:4px solid ${isEq ? '#10b981' : '#f59e0b'}; border-radius:6px; margin-bottom:1rem;">
      <strong>Summary:</strong> ${summary}
      <div style="margin-top:0.25rem; font-size:0.85rem;">
        Behavior Equivalence: <strong>${isEq ? 'VERIFIED (Preserved strictly: Moore = y₀ · Mealy)' : 'MISMATCH'}</strong>
      </div>
    </div>
  `;
  
  let html = '';
  steps.forEach(s => {
    html += `
      <div class="step-item">
        <div class="step-header">
          <span><strong>${s.title}</strong></span>
          <span class="badge badge-primary">Step ${s.step_number}</span>
        </div>
        <div class="step-body">
          <p>${s.description}</p>
    `;
    
    // Render special tables for step 1 or 2 if available
    if (s.details && s.details.splitting_table) {
      html += `
        <table class="data-table" style="margin-top:0.75rem;">
          <thead>
            <tr><th>Original State</th><th>Incoming Transition Outputs</th><th>Generated Split States</th><th>Theoretical Rationale</th></tr>
          </thead>
          <tbody>
      `;
      s.details.splitting_table.forEach(row => {
        html += `
          <tr>
            <td><strong>${row.original_state}</strong></td>
            <td>{${row.incoming_outputs.join(', ')}}</td>
            <td><strong>{${row.split_states.join(', ')}}</strong></td>
            <td style="text-align:left; font-size:0.8rem;">${row.reason}</td>
          </tr>
        `;
      });
      html += `</tbody></table>`;
    }
    
    if (s.details && s.details.mappings) {
      html += `<div class="step-code">`;
      s.details.mappings.slice(0, 10).forEach(m => {
        html += `${m.rule}\n`;
      });
      if (s.details.mappings.length > 10) {
        html += `... and ${s.details.mappings.length - 10} more mapped transitions.\n`;
      }
      html += `</div>`;
    }
    
    html += `</div></div>`;
  });
  
  elements.stepsContainer.innerHTML = html;
}

// Verification Table
function renderVerificationTable(results) {
  let html = '';
  results.forEach((r, idx) => {
    const isPass = r.equivalent;
    html += `
      <tr>
        <td><strong>T${String(idx + 1).padStart(2, '0')}</strong></td>
        <td><code>${r.input || 'ε'}</code></td>
        <td><code>${r.moore_output}</code></td>
        <td><code>${r.mealy_output}</code></td>
        <td><code>${r.expected_relation}</code></td>
        <td><span class="badge ${isPass ? 'badge-success' : 'badge-danger'}">${isPass ? 'PASS' : 'FAIL'}</span></td>
      </tr>
    `;
  });
  elements.verificationTableBody.innerHTML = html;
}

// Simulation Logic
async function startSimulation() {
  const inputStr = elements.inputString.value.trim();
  if (!state.sourceMachine || !state.convertedMachine) return;
  
  try {
    // Simulate on Source
    const resSource = await fetch('/api/simulate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        machine_type: state.sourceMachine.type,
        machine_data: state.sourceMachine,
        input_string: inputStr
      })
    });
    state.simSourceResult = await resSource.json();
    
    // Simulate on Converted
    const resConverted = await fetch('/api/simulate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        machine_type: state.convertedMachine.type,
        machine_data: state.convertedMachine,
        input_string: inputStr
      })
    });
    state.simConvertedResult = await resConverted.json();
    
    state.currentSimStep = 0;
    renderSimulationStep();
  } catch (err) {
    console.error("Simulation error:", err);
  }
}

function renderSimulationStep() {
  const srcRes = state.simSourceResult;
  const cvtRes = state.simConvertedResult;
  if (!srcRes || !cvtRes) return;
  
  const stepIdx = state.currentSimStep;
  const inputStr = elements.inputString.value.trim();
  
  // Render Input Tape
  let inHtml = '';
  for (let i = 0; i < inputStr.length; i++) {
    const isActive = (i === stepIdx - 1);
    const isPassed = (i < stepIdx - 1);
    inHtml += `
      <div class="tape-cell ${isActive ? 'active' : ''} ${isPassed ? 'passed' : ''}">
        <span>${inputStr[i]}</span>
        <span class="sub">#${i + 1}</span>
      </div>
    `;
  }
  if (!inputStr) {
    inHtml = `<div class="tape-cell active"><span>ε</span><span class="sub">empty</span></div>`;
  }
  elements.inputTapeCells.innerHTML = inHtml;
  
  // Render Source Tape Output
  renderTapeOutput(elements.sourceTapeCells, srcRes, state.sourceMachine.type, stepIdx);
  // Render Converted Tape Output
  renderTapeOutput(elements.convertedTapeCells, cvtRes, state.convertedMachine.type, stepIdx);
  
  // Determine active transitions for edge highlighting
  const srcStep = srcRes.steps[stepIdx] || null;
  const cvtStep = cvtRes.steps[stepIdx] || null;
  const srcActiveTransition = (srcStep && srcStep.current_state && srcStep.next_state)
    ? { from: srcStep.current_state, to: srcStep.next_state }
    : null;
  const cvtActiveTransition = (cvtStep && cvtStep.current_state && cvtStep.next_state)
    ? { from: cvtStep.current_state, to: cvtStep.next_state }
    : null;

  // Highlight active states AND active transitions in graphs
  const srcActiveState = srcRes.states_visited[stepIdx] || srcRes.states_visited[srcRes.states_visited.length - 1];
  const cvtActiveState = cvtRes.states_visited[stepIdx] || cvtRes.states_visited[cvtRes.states_visited.length - 1];
  
  renderSvgGraph(elements.sourceSvg, state.sourceMachine, srcActiveState, srcActiveTransition);
  renderSvgGraph(elements.convertedSvg, state.convertedMachine, cvtActiveState, cvtActiveTransition);
  
  // Log box
  const srcLogStep = srcRes.steps[stepIdx] || srcRes.steps[srcRes.steps.length - 1];
  const cvtLogStep = cvtRes.steps[stepIdx] || cvtRes.steps[cvtRes.steps.length - 1];

  // Compute accumulated outputs shown so far
  const srcOutSlice = srcRes.output_string.slice(0, stepIdx + (state.sourceMachine.type === 'Moore' ? 1 : 0));
  const cvtOutSlice = cvtRes.output_string.slice(0, stepIdx + (state.convertedMachine.type === 'Moore' ? 1 : 0));
  
  elements.simLogBox.innerHTML = `
    <div><strong>Step ${stepIdx} / ${Math.max(srcRes.steps.length - 1, 0)}:</strong></div>
    <div>• ${state.sourceMachine.type}: State <strong>${srcActiveState}</strong> | ${srcLogStep ? srcLogStep.description : 'Initial state'}</div>
    <div>• ${state.convertedMachine.type}: State <strong>${cvtActiveState}</strong> | ${cvtLogStep ? cvtLogStep.description : 'Initial state'}</div>
    <div style="margin-top:0.4rem; color:var(--primary); font-weight:600;">
      Simulated Source Output: <code>"${srcOutSlice || 'ε'}"</code>
      vs Converted Output: <code>"${cvtOutSlice || 'ε'}"</code>
    </div>
  `;
}

function renderTapeOutput(container, res, mType, currentStep) {
  let html = '';
  const outStr = res.output_string || '';

  // Moore: output has N+1 symbols (prefix + one per input).
  // Mealy: output has N symbols (one per transition).
  // visibleUpto = last index visible at this step.
  const visibleUpto = (mType === 'Moore') ? currentStep : (currentStep - 1);

  if (outStr.length === 0) {
    // No output yet or empty input string — show epsilon placeholder
    html = `<div class="tape-cell prefix-empty"><span>ε</span><span class="sub">no output</span></div>`;
  } else {
    for (let i = 0; i < outStr.length; i++) {
      const isPrefix = (mType === 'Moore' && i === 0);
      const isRevealed = (i <= visibleUpto);
      const isActive   = (i === visibleUpto) && isRevealed;
      const isPassed   = isRevealed && !isActive;

      let cellClass = 'tape-cell';
      if (isPrefix)  cellClass += ' prefix-cell';
      if (isActive)  cellClass += ' active';
      if (isPassed)  cellClass += ' passed';

      const sub = isPrefix ? 'init λ(q₀)' : `z${i}`;

      html += `
        <div class="${cellClass}">
          <span>${isRevealed ? outStr[i] : '•'}</span>
          <span class="sub">${sub}</span>
        </div>
      `;
    }
  }
  container.innerHTML = html;
}

function stepForward() {
  if (!state.simSourceResult) return;
  const maxSteps = Math.max(state.simSourceResult.steps.length - 1, 0);
  if (state.currentSimStep < maxSteps) {
    state.currentSimStep++;
    renderSimulationStep();
  } else {
    pausePlay();
  }
}

function stepBack() {
  if (state.currentSimStep > 0) {
    state.currentSimStep--;
    renderSimulationStep();
  }
}

function resetSimulation() {
  pausePlay();
  state.currentSimStep = 0;
  renderSimulationStep();
}

function togglePlayPause() {
  if (state.isPlaying) {
    pausePlay();
  } else {
    startPlay();
  }
}

function startPlay() {
  state.isPlaying = true;
  elements.btnPlayPause.textContent = '⏸ Pause';
  state.playTimer = setInterval(() => {
    if (!state.simSourceResult) return;
    const maxSteps = Math.max(state.simSourceResult.steps.length - 1, 0);
    if (state.currentSimStep >= maxSteps) {
      state.currentSimStep = 0;
    }
    stepForward();
  }, state.playSpeedMs);
}

function pausePlay() {
  state.isPlaying = false;
  elements.btnPlayPause.textContent = '▶ Play';
  if (state.playTimer) {
    clearInterval(state.playTimer);
    state.playTimer = null;
  }
}

function clearSimulation() {
  pausePlay();
  state.simSourceResult = null;
  state.simConvertedResult = null;
  state.currentSimStep = 0;
  elements.inputTapeCells.innerHTML = '';
  elements.sourceTapeCells.innerHTML = '';
  elements.convertedTapeCells.innerHTML = '';
  elements.simLogBox.innerHTML = 'Enter an input string and click "Simulate" to begin step-by-step playback.';
}

function clearSteps() {
  elements.stepsContainer.innerHTML = '';
  elements.conversionSummary.innerHTML = '';
}

// Verification Tests
async function runAllVerificationTests() {
  if (!state.sourceMachine || !state.convertedMachine) {
    alert("Please convert the machine first before running verification tests.");
    return;
  }
  
  const mooreData = (state.sourceMachine.type === 'Moore') ? state.sourceMachine : state.convertedMachine;
  const mealyData = (state.sourceMachine.type === 'Mealy') ? state.sourceMachine : state.convertedMachine;
  
  const testSuite = [
    "", "0", "1", "00", "01", "10", "11",
    "010", "101", "00110", "1101", "10101", "111000", "010101"
  ];
  
  try {
    const res = await fetch('/api/verify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        moore_data: mooreData,
        mealy_data: mealyData,
        test_strings: testSuite
      })
    });
    const data = await res.json();
    renderVerificationTable(data.test_results);
  } catch (err) {
    console.error("Verification test failed:", err);
  }
}

// Image Upload, Screenshot Paste & Auto-Conversion
let lastImageUploadData = null;

function handleImageUpload(e) {
  const file = e.target.files[0];
  if (!file) return;
  processImageBlob(file);
  e.target.value = '';
}

async function handlePasteButtonClick() {
  // Try modern Clipboard API
  if (navigator.clipboard && navigator.clipboard.read) {
    try {
      const items = await navigator.clipboard.read();
      for (const item of items) {
        for (const type of item.types) {
          if (type.startsWith('image/')) {
            const blob = await item.getType(type);
            processImageBlob(blob);
            return;
          }
        }
      }
    } catch (err) {
      console.log("Clipboard read permission not granted or no image in clipboard, falling back to modal prompt:", err);
    }
  }

  // Open modal and show paste invitation
  elements.imageOcrModal.classList.add('active');
  elements.imageOcrLoading.style.display = 'none';
  elements.imageOcrResultContent.style.display = 'block';
  elements.ocrDetectedBadge.textContent = 'Ready to Paste Screenshot';
  elements.ocrSummaryText.textContent = 'Press Ctrl+V on your keyboard now to paste the copied screenshot directly!';
  elements.ocrRawLines.textContent = 'Waiting for Ctrl+V clipboard paste...';
  elements.ocrMachineOverview.innerHTML = '<em>Take a screenshot (e.g. Win+Shift+S) and press Ctrl+V.</em>';
  elements.btnApplyImageConversion.disabled = true;
}

function handleGlobalPaste(e) {
  const clipboardData = e.clipboardData || window.clipboardData;
  if (!clipboardData) return;

  const items = clipboardData.items;
  for (let i = 0; i < items.length; i++) {
    if (items[i].type.indexOf('image') !== -1) {
      const blob = items[i].getAsFile();
      if (blob) {
        e.preventDefault();
        processImageBlob(blob);
        break;
      }
    }
  }
}

async function processImageBlob(fileOrBlob) {
  // Open modal in loading state
  elements.imageOcrModal.classList.add('active');
  elements.imageOcrLoading.style.display = 'block';
  elements.imageOcrResultContent.style.display = 'none';
  elements.btnApplyImageConversion.disabled = true;

  const formData = new FormData();
  const filename = fileOrBlob.name || "pasted_screenshot.png";
  formData.append('file', fileOrBlob, filename);

  try {
    const res = await fetch('/api/upload-image', {
      method: 'POST',
      body: formData
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Failed to process image');
    }

    const data = await res.json();
    lastImageUploadData = data;

    // Display OCR results
    elements.imageOcrLoading.style.display = 'none';
    elements.imageOcrResultContent.style.display = 'block';
    elements.btnApplyImageConversion.disabled = false;

    elements.ocrDetectedBadge.textContent = `Detected: ${data.detected_type} Machine`;
    elements.ocrSummaryText.textContent = `Extracted ${data.machine_data.states.length} states: {${data.machine_data.states.join(', ')}}, start state: ${data.machine_data.start_state}`;

    elements.ocrRawLines.textContent = data.raw_text.join('\n') || '(No text)';

    let overview = `<strong>Automaton:</strong> ${data.machine_data.name} (${data.detected_type})<br>`;
    overview += `<strong>States Q:</strong> {${data.machine_data.states.join(', ')}}<br>`;
    overview += `<strong>Alphabet Σ:</strong> {${data.machine_data.input_alphabet.join(', ')}}<br>`;
    overview += `<strong>Transitions:</strong> ${data.machine_data.transitions.length} defined<br>`;
    overview += `<strong>Target Equivalent:</strong> ${data.converted.type} with ${data.converted.states.length} states (Equivalence verified: ${data.equivalence_verified})`;
    elements.ocrMachineOverview.innerHTML = overview;

  } catch (err) {
    elements.imageOcrLoading.style.display = 'none';
    elements.imageOcrResultContent.style.display = 'block';
    elements.ocrDetectedBadge.textContent = `Error Processing Image`;
    elements.ocrSummaryText.textContent = err.message;
    elements.ocrRawLines.textContent = 'Please make sure the image or screenshot is clear and contains a state transition table or diagram.';
    elements.ocrMachineOverview.innerHTML = '<span style="color:var(--danger)">Parsing failed. Please check the image or enter transitions manually via "+ Custom Machine".</span>';
  }
}

function applyImageConversion() {
  if (!lastImageUploadData) return;
  const data = lastImageUploadData;

  state.sourceMachine = data.machine_data;
  state.convertedMachine = data.converted;
  state.conversionReport = data;
  state.mode = (data.detected_type === 'Moore') ? 'MooreToMealy' : 'MealyToMoore';

  if (state.mode === 'MooreToMealy') {
    elements.toggleMooreToMealy.classList.add('active');
    elements.toggleMealyToMoore.classList.remove('active');
    elements.startOutputContainer.style.display = 'none';
  } else {
    elements.toggleMealyToMoore.classList.add('active');
    elements.toggleMooreToMealy.classList.remove('active');
    elements.startOutputContainer.style.display = 'flex';
  }

  renderSourceMachine();
  renderConvertedMachine();
  renderConversionSteps(data.steps, data.summary, data.equivalence_verified);
  renderVerificationTable(data.test_results);

  elements.imageOcrModal.classList.remove('active');
  startSimulation();
}

// JSON Export / Import
function exportMachineJson() {
  if (!state.sourceMachine) return;
  const blob = new Blob([JSON.stringify(state.sourceMachine, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${state.sourceMachine.name.replace(/\s+/g, '_')}.json`;
  a.click();
  URL.revokeObjectURL(url);
}

function handleImportJson(e) {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (evt) => {
    try {
      const data = JSON.parse(evt.target.result);
      if (!data.type || !data.states || !data.transitions) {
        throw new Error("Invalid automata JSON schema.");
      }
      state.sourceMachine = data;
      state.mode = (data.type === 'Moore') ? 'MooreToMealy' : 'MealyToMoore';
      setMode(state.mode, false);
      renderSourceMachine();
      clearConvertedMachine();
      runConversion();
    } catch (err) {
      alert(`Import error: ${err.message}`);
    }
  };
  reader.readAsText(file);
  e.target.value = '';
}

// Custom Modal Handling
function openCustomModal() {
  elements.customModal.classList.add('active');
  updateCustomFieldsPlaceholder();
}

function closeCustomModal() {
  elements.customModal.classList.remove('active');
}

function updateCustomFieldsPlaceholder() {
  const type = elements.customMachineType.value;
  if (type === 'Moore') {
    elements.customDefinitionArea.placeholder = 
`# Moore Machine Transitions & State Outputs
# Format: State -> Output
q0 -> 0
q1 -> 1

# Transitions Format: from_state, input_symbol -> to_state
q0, 0 -> q0
q0, 1 -> q1
q1, 0 -> q0
q1, 1 -> q1`;
  } else {
    elements.customDefinitionArea.placeholder = 
`# Mealy Machine Transitions
# Format: from_state, input_symbol -> to_state, output_symbol
q0, 0 -> q0, 1
q0, 1 -> q1, 0
q1, 0 -> q0, 1
q1, 1 -> q1, 0`;
  }
}

function saveCustomMachine() {
  try {
    const type = elements.customMachineType.value;
    const name = elements.customMachineName.value.trim() || `Custom ${type}`;
    const states = elements.customStates.value.split(',').map(s => s.trim()).filter(Boolean);
    const alphabet = elements.customAlphabet.value.split(',').map(s => s.trim()).filter(Boolean);
    const outputs = elements.customOutputs.value.split(',').map(s => s.trim()).filter(Boolean);
    const startState = elements.customStartState.value.trim();
    
    const lines = elements.customDefinitionArea.value.split('\n');
    const transitions = [];
    const stateOutputs = {};
    
    lines.forEach(line => {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith('#')) return;
      
      if (type === 'Moore' && trimmed.includes('->') && !trimmed.includes(',')) {
        // State output line: "q0 -> 1"
        const [st, out] = trimmed.split('->').map(s => s.trim());
        stateOutputs[st] = out;
      } else if (trimmed.includes('->')) {
        const [lhs, rhs] = trimmed.split('->').map(s => s.trim());
        const [fromSt, sym] = lhs.split(',').map(s => s.trim());
        
        if (type === 'Moore') {
          transitions.push({ from: fromSt, symbol: sym, to: rhs });
        } else {
          const [toSt, outSym] = rhs.split(',').map(s => s.trim());
          transitions.push({ from: fromSt, symbol: sym, to: toSt, output: outSym });
        }
      }
    });
    
    const customObj = {
      type: type,
      name: name,
      states: states,
      input_alphabet: alphabet,
      output_alphabet: outputs,
      start_state: startState,
      transitions: transitions
    };
    if (type === 'Moore') {
      customObj.state_outputs = stateOutputs;
    }
    
    state.sourceMachine = customObj;
    setMode(type === 'Moore' ? 'MooreToMealy' : 'MealyToMoore', false);
    renderSourceMachine();
    closeCustomModal();
    runConversion();
  } catch (err) {
    alert(`Format error in definition: ${err.message}`);
  }
}

// ==========================================================================
// VISUAL DIAGRAM STUDIO (MANUAL DIAGRAM CREATOR) IMPLEMENTATION
// ==========================================================================

const studioState = {
  type: 'Mealy', // 'Mealy' or 'Moore'
  states: ['S1', 'S2', 'S3'],
  nodePositions: {
    'S1': { x: 140, y: 190 },
    'S2': { x: 320, y: 190 },
    'S3': { x: 230, y: 320 }
  },
  stateOutputs: { 'S1': '0', 'S2': '0', 'S3': '1' },
  transitions: [
    { from: 'S1', symbol: '0', to: 'S1', output: '0' },
    { from: 'S1', symbol: '1', to: 'S2', output: '0' },
    { from: 'S2', symbol: '0', to: 'S3', output: '0' },
    { from: 'S2', symbol: '1', to: 'S2', output: '0' },
    { from: 'S3', symbol: '0', to: 'S1', output: '0' },
    { from: 'S3', symbol: '1', to: 'S2', output: '1' }
  ],
  startState: 'S1',
  activeTool: 'select', // 'select', 'addState', 'addTransition', 'delete'
  selectedNode: null,
  transitionSourceNode: null,
  isDragging: false,
  draggedNode: null,
  dragOffset: { x: 0, y: 0 },
  pendingTransitionNodes: null // { from, to }
};

// Open Studio fresh or with templates
function openDiagramStudioNew() {
  // If source machine exists, ask or pre-fill with current
  if (state.sourceMachine && state.sourceMachine.states && state.sourceMachine.states.length > 0) {
    loadMachineIntoStudio(state.sourceMachine);
  } else {
    initDefaultStudioMachine('Mealy');
  }
  elements.diagramStudioModal.classList.add('active');
  setStudioTool('select');
  setTimeout(() => {
    studioAutoArrange();
    renderStudioSvg();
    renderStudioLiveTable();
    renderStudioInspector();
  }, 100);
}

// Open Studio editing current loaded source machine
function openDiagramStudioEditCurrent() {
  if (state.sourceMachine) {
    loadMachineIntoStudio(state.sourceMachine);
  } else {
    initDefaultStudioMachine('Mealy');
  }
  elements.diagramStudioModal.classList.add('active');
  setStudioTool('select');
  setTimeout(() => {
    renderStudioSvg();
    renderStudioLiveTable();
    renderStudioInspector();
  }, 100);
}

function closeDiagramStudio() {
  elements.diagramStudioModal.classList.remove('active');
  studioState.isDragging = false;
  studioState.draggedNode = null;
  studioState.transitionSourceNode = null;
}

function initDefaultStudioMachine(type = 'Mealy') {
  studioState.type = type;
  elements.studioMachineType.value = type;
  studioState.states = ['S1', 'S2'];
  studioState.nodePositions = {
    'S1': { x: 180, y: 220 },
    'S2': { x: 380, y: 220 }
  };
  studioState.stateOutputs = { 'S1': '0', 'S2': '1' };
  studioState.startState = 'S1';
  studioState.selectedNode = 'S1';
  studioState.transitionSourceNode = null;
  if (type === 'Mealy') {
    studioState.transitions = [
      { from: 'S1', symbol: '0', to: 'S1', output: '0' },
      { from: 'S1', symbol: '1', to: 'S2', output: '1' },
      { from: 'S2', symbol: '0', to: 'S1', output: '0' },
      { from: 'S2', symbol: '1', to: 'S2', output: '0' }
    ];
  } else {
    studioState.transitions = [
      { from: 'S1', symbol: '0', to: 'S1' },
      { from: 'S1', symbol: '1', to: 'S2' },
      { from: 'S2', symbol: '0', to: 'S1' },
      { from: 'S2', symbol: '1', to: 'S2' }
    ];
  }
}

function loadMachineIntoStudio(m) {
  studioState.type = m.type || 'Mealy';
  elements.studioMachineType.value = studioState.type;
  studioState.states = [...m.states];
  studioState.startState = m.start_state || m.states[0];
  studioState.stateOutputs = m.state_outputs ? { ...m.state_outputs } : {};
  studioState.transitions = JSON.parse(JSON.stringify(m.transitions || []));
  studioState.selectedNode = studioState.startState;
  studioState.transitionSourceNode = null;

  // Compute neat layout positions
  const svgW = elements.studioSvg.clientWidth || 600;
  const svgH = elements.studioSvg.clientHeight || 450;
  const cx = svgW / 2;
  const cy = svgH / 2;
  const radius = Math.min(cx, cy) - 75;
  const n = studioState.states.length;
  studioState.nodePositions = {};

  studioState.states.forEach((st, idx) => {
    const angle = (2 * Math.PI * idx) / n - Math.PI / 2;
    studioState.nodePositions[st] = {
      x: cx + radius * Math.cos(angle),
      y: cy + radius * Math.sin(angle)
    };
  });
}

function handleStudioTypeChange() {
  const newType = elements.studioMachineType.value;
  studioState.type = newType;
  if (newType === 'Moore') {
    // Add default outputs if missing
    studioState.states.forEach(st => {
      if (!studioState.stateOutputs[st]) {
        studioState.stateOutputs[st] = '0';
      }
    });
    // Remove transition outputs
    studioState.transitions.forEach(t => {
      delete t.output;
    });
  } else {
    // Mealy: add default outputs on transitions
    studioState.transitions.forEach(t => {
      if (t.output === undefined) {
        t.output = '0';
      }
    });
  }
  renderStudioSvg();
  renderStudioLiveTable();
  renderStudioInspector();
}

function setStudioTool(toolName) {
  studioState.activeTool = toolName;
  studioState.transitionSourceNode = null;

  elements.toolSelect.classList.toggle('active', toolName === 'select');
  elements.toolAddState.classList.toggle('active', toolName === 'addState');
  elements.toolAddTransition.classList.toggle('active', toolName === 'addTransition');
  elements.toolDelete.classList.toggle('active', toolName === 'delete');

  if (toolName === 'select') {
    elements.studioSvg.style.cursor = 'default';
    elements.studioCanvasHint.textContent = '👆 Click a state to inspect or drag it to reposition.';
  } else if (toolName === 'addState') {
    elements.studioSvg.style.cursor = 'crosshair';
    elements.studioCanvasHint.textContent = '🔘 Click anywhere on the canvas to place a new state circle.';
  } else if (toolName === 'addTransition') {
    elements.studioSvg.style.cursor = 'pointer';
    elements.studioCanvasHint.textContent = '➡️ Click the SOURCE state, then click the TARGET state (or same state for self-loop).';
  } else if (toolName === 'delete') {
    elements.studioSvg.style.cursor = 'not-allowed';
    elements.studioCanvasHint.textContent = '🗑️ Click any state node or transition edge to delete it.';
  }
  renderStudioSvg();
}

function studioAutoArrange() {
  const svgW = elements.studioSvg.clientWidth || 600;
  const svgH = elements.studioSvg.clientHeight || 450;
  const cx = svgW / 2;
  const cy = svgH / 2;
  const radius = Math.min(cx, cy) - 75;
  const n = studioState.states.length;

  studioState.states.forEach((st, idx) => {
    const angle = (2 * Math.PI * idx) / n - Math.PI / 2;
    studioState.nodePositions[st] = {
      x: cx + radius * Math.cos(angle),
      y: cy + radius * Math.sin(angle)
    };
  });
  renderStudioSvg();
}

function studioClearCanvas() {
  if (confirm("Clear all states and transitions from the canvas?")) {
    studioState.states = [];
    studioState.nodePositions = {};
    studioState.stateOutputs = {};
    studioState.transitions = [];
    studioState.startState = '';
    studioState.selectedNode = null;
    studioState.transitionSourceNode = null;
    renderStudioSvg();
    renderStudioLiveTable();
    renderStudioInspector();
  }
}

// SVG Drawing for Studio Canvas
function renderStudioSvg() {
  const svg = elements.studioSvg;
  svg.innerHTML = '';
  const width = svg.clientWidth || 600;
  const height = svg.clientHeight || 450;
  svg.setAttribute('viewBox', `0 0 ${width} ${height}`);

  // Arrow markers
  const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
  defs.innerHTML = `
    <marker id="studio-arrow" viewBox="0 0 10 10" refX="24" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#475569" />
    </marker>
    <marker id="studio-arrow-active" viewBox="0 0 10 10" refX="24" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#2563eb" />
    </marker>
  `;
  svg.appendChild(defs);

  // Group transitions by pair (from -> to)
  const edgeGroups = {};
  studioState.transitions.forEach((t, idx) => {
    const key = `${t.from}->${t.to}`;
    if (!edgeGroups[key]) edgeGroups[key] = [];
    edgeGroups[key].push({ ...t, origIndex: idx });
  });

  const edgesG = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  svg.appendChild(edgesG);

  // Draw transition paths
  for (const [key, tList] of Object.entries(edgeGroups)) {
    const [fromNode, toNode] = key.split('->');
    const p1 = studioState.nodePositions[fromNode];
    const p2 = studioState.nodePositions[toNode];
    if (!p1 || !p2) continue;

    let label = '';
    if (studioState.type === 'Moore') {
      label = tList.map(t => t.symbol).join(', ');
    } else {
      label = tList.map(t => `${t.symbol}/${t.output || '0'}`).join(', ');
    }

    if (fromNode === toNode) {
      // Self-loop
      const angle = -Math.PI / 2; // Point upwards
      const loopCenterX = p1.x;
      const loopCenterY = p1.y - 38;

      const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      const x1 = p1.x - 14;
      const y1 = p1.y - 18;
      const x2 = p1.x + 14;
      const y2 = p1.y - 18;

      path.setAttribute('d', `M ${x1} ${y1} C ${loopCenterX - 22} ${loopCenterY - 18}, ${loopCenterX + 22} ${loopCenterY - 18}, ${x2} ${y2}`);
      path.setAttribute('fill', 'none');
      path.setAttribute('stroke', '#64748b');
      path.setAttribute('stroke-width', '2.5');
      path.setAttribute('marker-end', 'url(#studio-arrow)');
      path.style.cursor = (studioState.activeTool === 'delete') ? 'pointer' : 'default';

      if (studioState.activeTool === 'delete') {
        path.addEventListener('click', (e) => {
          e.stopPropagation();
          deleteTransitionsBetween(fromNode, toNode);
        });
      }
      edgesG.appendChild(path);

      // Label
      const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      text.setAttribute('x', loopCenterX);
      text.setAttribute('y', loopCenterY - 4);
      text.setAttribute('text-anchor', 'middle');
      text.setAttribute('fill', '#1e293b');
      text.setAttribute('font-size', '11');
      text.setAttribute('font-weight', '700');
      text.setAttribute('paint-order', 'stroke');
      text.setAttribute('stroke', '#ffffff');
      text.setAttribute('stroke-width', '3');
      text.textContent = label;
      if (studioState.activeTool === 'delete') {
        text.style.cursor = 'pointer';
        text.addEventListener('click', (e) => {
          e.stopPropagation();
          deleteTransitionsBetween(fromNode, toNode);
        });
      }
      edgesG.appendChild(text);
    } else {
      // Directed arc between two states
      const dx = p2.x - p1.x;
      const dy = p2.y - p1.y;
      const dist = Math.sqrt(dx * dx + dy * dy);

      // Check if reverse edge exists for dual curvature
      const reverseKey = `${toNode}->${fromNode}`;
      const curvature = edgeGroups[reverseKey] ? 28 : 16;
      const nx = -dy / dist;
      const ny = dx / dist;
      const cx = (p1.x + p2.x) / 2 + nx * curvature;
      const cy = (p1.y + p2.y) / 2 + ny * curvature;

      const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      path.setAttribute('d', `M ${p1.x} ${p1.y} Q ${cx} ${cy} ${p2.x} ${p2.y}`);
      path.setAttribute('fill', 'none');
      path.setAttribute('stroke', '#64748b');
      path.setAttribute('stroke-width', '2.5');
      path.setAttribute('marker-end', 'url(#studio-arrow)');
      path.style.cursor = (studioState.activeTool === 'delete') ? 'pointer' : 'default';

      if (studioState.activeTool === 'delete') {
        path.addEventListener('click', (e) => {
          e.stopPropagation();
          deleteTransitionsBetween(fromNode, toNode);
        });
      }
      edgesG.appendChild(path);

      // Label text
      const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      text.setAttribute('x', cx);
      text.setAttribute('y', cy);
      text.setAttribute('text-anchor', 'middle');
      text.setAttribute('fill', '#0f172a');
      text.setAttribute('font-size', '11');
      text.setAttribute('font-weight', '700');
      text.setAttribute('paint-order', 'stroke');
      text.setAttribute('stroke', '#ffffff');
      text.setAttribute('stroke-width', '3.5');
      text.textContent = label;
      if (studioState.activeTool === 'delete') {
        text.style.cursor = 'pointer';
        text.addEventListener('click', (e) => {
          e.stopPropagation();
          deleteTransitionsBetween(fromNode, toNode);
        });
      }
      edgesG.appendChild(text);
    }
  }

  // Draw state nodes
  const nodesG = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  svg.appendChild(nodesG);

  studioState.states.forEach(stateName => {
    const pos = studioState.nodePositions[stateName] || { x: 100, y: 100 };
    const isStart = (stateName === studioState.startState);
    const isSelected = (stateName === studioState.selectedNode);
    const isConnectingSource = (stateName === studioState.transitionSourceNode);

    const nodeG = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    nodeG.setAttribute('data-node', stateName);

    // Start state arrow
    if (isStart) {
      const startArrow = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      startArrow.setAttribute('d', `M ${pos.x - 48} ${pos.y} L ${pos.x - 24} ${pos.y}`);
      startArrow.setAttribute('stroke', '#2563eb');
      startArrow.setAttribute('stroke-width', '3');
      startArrow.setAttribute('marker-end', 'url(#studio-arrow-active)');
      nodeG.appendChild(startArrow);

      const startText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      startText.setAttribute('x', pos.x - 52);
      startText.setAttribute('y', pos.y + 4);
      startText.setAttribute('text-anchor', 'end');
      startText.setAttribute('fill', '#2563eb');
      startText.setAttribute('font-size', '10');
      startText.setAttribute('font-weight', '700');
      startText.textContent = 'Start';
      nodeG.appendChild(startText);
    }

    // Node Circle
    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle.setAttribute('cx', pos.x);
    circle.setAttribute('cy', pos.y);
    circle.setAttribute('r', '24');
    circle.setAttribute('fill', isConnectingSource ? '#fef3c7' : (isSelected ? '#eff6ff' : '#ffffff'));
    circle.setAttribute('stroke', isConnectingSource ? '#d97706' : (isSelected ? '#2563eb' : '#475569'));
    circle.setAttribute('stroke-width', (isSelected || isConnectingSource) ? '3.5' : '2.5');

    if (isConnectingSource) {
      circle.setAttribute('stroke-dasharray', '4,2');
    }
    if (isSelected) {
      circle.setAttribute('filter', 'drop-shadow(0 0 6px rgba(37,99,235,0.4))');
    }

    // Cursor styling
    if (studioState.activeTool === 'select') {
      circle.style.cursor = 'grab';
    } else if (studioState.activeTool === 'addTransition') {
      circle.style.cursor = 'pointer';
    } else if (studioState.activeTool === 'delete') {
      circle.style.cursor = 'not-allowed';
    }
    nodeG.appendChild(circle);

    // State Name Label
    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('x', pos.x);
    text.setAttribute('y', studioState.type === 'Moore' ? pos.y - 2 : pos.y + 4);
    text.setAttribute('text-anchor', 'middle');
    text.setAttribute('fill', '#0f172a');
    text.setAttribute('font-size', '12');
    text.setAttribute('font-weight', '700');
    text.setAttribute('pointer-events', 'none');
    text.textContent = stateName;
    nodeG.appendChild(text);

    // Moore State Output Label
    if (studioState.type === 'Moore') {
      const outText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      outText.setAttribute('x', pos.x);
      outText.setAttribute('y', pos.y + 13);
      outText.setAttribute('text-anchor', 'middle');
      outText.setAttribute('fill', '#dc2626');
      outText.setAttribute('font-size', '10');
      outText.setAttribute('font-weight', '700');
      outText.setAttribute('pointer-events', 'none');
      outText.textContent = `/${studioState.stateOutputs[stateName] || '0'}`;
      nodeG.appendChild(outText);
    }

    nodesG.appendChild(nodeG);
  });
}

function deleteTransitionsBetween(from, to) {
  studioState.transitions = studioState.transitions.filter(t => !(t.from === from && t.to === to));
  renderStudioSvg();
  renderStudioLiveTable();
}

// Studio Canvas Event Handlers
function handleStudioCanvasClick(e) {
  const rect = elements.studioSvg.getBoundingClientRect();
  const clickX = e.clientX - rect.left;
  const clickY = e.clientY - rect.top;

  // Check if click was on a state circle
  const targetNodeEl = e.target.closest('[data-node]');
  const clickedNodeName = targetNodeEl ? targetNodeEl.getAttribute('data-node') : null;

  if (studioState.activeTool === 'addState') {
    if (!clickedNodeName) {
      // Place a new state
      let prefix = 'S';
      let count = studioState.states.length + 1;
      let newName = `${prefix}${count}`;
      while (studioState.states.includes(newName)) {
        count++;
        newName = `${prefix}${count}`;
      }

      studioState.states.push(newName);
      studioState.nodePositions[newName] = { x: Math.round(clickX), y: Math.round(clickY) };
      studioState.stateOutputs[newName] = '0';
      if (studioState.states.length === 1) {
        studioState.startState = newName;
      }
      studioState.selectedNode = newName;
      renderStudioSvg();
      renderStudioLiveTable();
      renderStudioInspector();
    }
  } else if (studioState.activeTool === 'addTransition') {
    if (clickedNodeName) {
      if (!studioState.transitionSourceNode) {
        // Step 1: select source node
        studioState.transitionSourceNode = clickedNodeName;
        elements.studioCanvasHint.textContent = `Source state set to '${clickedNodeName}'. Now click destination state (or click '${clickedNodeName}' for self-loop).`;
        renderStudioSvg();
      } else {
        // Step 2: select target node -> open prompt
        const src = studioState.transitionSourceNode;
        const dst = clickedNodeName;
        studioState.transitionSourceNode = null;
        elements.studioCanvasHint.textContent = `Connecting '${src}' ➔ '${dst}'...`;
        openTransitionPrompt(src, dst);
      }
    }
  } else if (studioState.activeTool === 'delete') {
    if (clickedNodeName) {
      // Delete the clicked state and all its connected edges
      const doomed = clickedNodeName;
      studioState.states = studioState.states.filter(s => s !== doomed);
      delete studioState.nodePositions[doomed];
      delete studioState.stateOutputs[doomed];
      studioState.transitions = studioState.transitions.filter(t => t.from !== doomed && t.to !== doomed);

      if (studioState.startState === doomed) {
        studioState.startState = studioState.states[0] || '';
      }
      if (studioState.selectedNode === doomed) {
        studioState.selectedNode = studioState.states[0] || null;
      }
      renderStudioSvg();
      renderStudioLiveTable();
      renderStudioInspector();
    }
  } else if (studioState.activeTool === 'select') {
    if (clickedNodeName) {
      studioState.selectedNode = clickedNodeName;
      renderStudioSvg();
      renderStudioInspector();
    }
  }
}

function handleStudioCanvasMouseDown(e) {
  if (studioState.activeTool !== 'select') return;
  const targetNodeEl = e.target.closest('[data-node]');
  if (targetNodeEl) {
    const nodeName = targetNodeEl.getAttribute('data-node');
    studioState.isDragging = true;
    studioState.draggedNode = nodeName;
    studioState.selectedNode = nodeName;
    const pos = studioState.nodePositions[nodeName] || { x: 0, y: 0 };
    const rect = elements.studioSvg.getBoundingClientRect();
    studioState.dragOffset = {
      x: (e.clientX - rect.left) - pos.x,
      y: (e.clientY - rect.top) - pos.y
    };
    elements.studioSvg.style.cursor = 'grabbing';
    renderStudioInspector();
  }
}

function handleStudioCanvasMouseMove(e) {
  if (!studioState.isDragging || !studioState.draggedNode) return;
  const rect = elements.studioSvg.getBoundingClientRect();
  const mouseX = e.clientX - rect.left;
  const mouseY = e.clientY - rect.top;

  const newX = Math.max(30, Math.min(rect.width - 30, mouseX - studioState.dragOffset.x));
  const newY = Math.max(30, Math.min(rect.height - 30, mouseY - studioState.dragOffset.y));

  studioState.nodePositions[studioState.draggedNode] = { x: newX, y: newY };
  renderStudioSvg();
}

function handleStudioCanvasMouseUp() {
  if (studioState.isDragging) {
    studioState.isDragging = false;
    studioState.draggedNode = null;
    if (studioState.activeTool === 'select') {
      elements.studioSvg.style.cursor = 'default';
    }
  }
}

// Transition Prompt Logic
function openTransitionPrompt(fromNode, toNode) {
  studioState.pendingTransitionNodes = { from: fromNode, to: toNode };
  elements.transPromptTitle.textContent = `Add Transition: ${fromNode} ➔ ${toNode}`;

  // Find next unused input symbol for fromNode
  const existingInputs = studioState.transitions.filter(t => t.from === fromNode).map(t => t.symbol);
  if (!existingInputs.includes('0')) {
    elements.promptInputSymbol.value = '0';
  } else if (!existingInputs.includes('1')) {
    elements.promptInputSymbol.value = '1';
  } else {
    elements.promptInputSymbol.value = '0';
  }

  if (studioState.type === 'Mealy') {
    elements.promptOutputContainer.style.display = 'block';
    elements.promptOutputSymbol.value = '0';
  } else {
    elements.promptOutputContainer.style.display = 'none';
  }

  elements.transitionPromptModal.classList.add('active');
  elements.promptInputSymbol.focus();
}

function closeTransitionPrompt() {
  elements.transitionPromptModal.classList.remove('active');
  studioState.pendingTransitionNodes = null;
  setStudioTool('select');
}

function confirmTransitionPrompt() {
  if (!studioState.pendingTransitionNodes) return;
  const sym = elements.promptInputSymbol.value.trim();
  const out = elements.promptOutputSymbol.value.trim() || '0';

  if (!sym) {
    alert("Please enter an input symbol (e.g. 0, 1, a).");
    return;
  }

  const { from, to } = studioState.pendingTransitionNodes;

  // If transition for (from, sym) already exists, update destination & output
  const existingIdx = studioState.transitions.findIndex(t => t.from === from && t.symbol === sym);
  if (existingIdx >= 0) {
    studioState.transitions[existingIdx].to = to;
    if (studioState.type === 'Mealy') {
      studioState.transitions[existingIdx].output = out;
    }
  } else {
    const newTrans = { from, symbol: sym, to };
    if (studioState.type === 'Mealy') {
      newTrans.output = out;
    }
    studioState.transitions.push(newTrans);
  }

  closeTransitionPrompt();
  renderStudioSvg();
  renderStudioLiveTable();
}

// Live Transition Table in Studio
function renderStudioLiveTable() {
  const container = elements.studioLiveTable;
  if (studioState.states.length === 0) {
    container.innerHTML = `<p style="color:var(--text-muted); padding:0.5rem;">No states defined. Click "+ Add State" to begin.</p>`;
    return;
  }

  // Derive input alphabet from transitions
  const inputSet = new Set(studioState.transitions.map(t => t.symbol));
  if (inputSet.size === 0) {
    inputSet.add('0');
    inputSet.add('1');
  }
  const inputAlphabet = Array.from(inputSet).sort();

  // Build lookup
  const transMap = {};
  studioState.transitions.forEach(t => {
    transMap[`${t.from},${t.symbol}`] = t;
  });

  let html = `<table class="data-table" style="font-size:0.75rem;"><thead><tr><th>State</th>`;
  if (studioState.type === 'Moore') {
    html += `<th>Output</th>`;
    inputAlphabet.forEach(a => html += `<th>Next (a=${a})</th>`);
  } else {
    inputAlphabet.forEach(a => html += `<th>In ${a} (Next, Out)</th>`);
  }
  html += `</tr></thead><tbody>`;

  let missingCount = 0;
  studioState.states.forEach(q => {
    const isStart = (q === studioState.startState);
    html += `<tr class="${isStart ? 'start-state-row' : ''}">`;
    html += `<td class="state-col"><strong>${q}</strong></td>`;

    if (studioState.type === 'Moore') {
      const out = studioState.stateOutputs[q] || '0';
      html += `<td>${out}</td>`;
      inputAlphabet.forEach(a => {
        const t = transMap[`${q},${a}`];
        if (t) {
          html += `<td>${t.to}</td>`;
        } else {
          missingCount++;
          html += `<td style="color:var(--danger); font-weight:bold;">?</td>`;
        }
      });
    } else {
      inputAlphabet.forEach(a => {
        const t = transMap[`${q},${a}`];
        if (t) {
          html += `<td>(${t.to}, ${t.output || '0'})</td>`;
        } else {
          missingCount++;
          html += `<td style="color:var(--danger); font-weight:bold;">?</td>`;
        }
      });
    }
    html += `</tr>`;
  });
  html += `</tbody></table>`;

  if (missingCount > 0) {
    html += `
      <div style="margin-top:0.5rem; color:var(--warning); font-size:0.75rem; font-weight:600;">
        ⚠️ ${missingCount} transition(s) undefined. Add them or they will default to self-loops.
      </div>
    `;
  } else {
    html += `
      <div style="margin-top:0.5rem; color:var(--success); font-size:0.75rem; font-weight:600;">
        ✓ Fully deterministic transition matrix!
      </div>
    `;
  }

  container.innerHTML = html;
}

// Studio Inspector for Selected Node
function renderStudioInspector() {
  const container = elements.studioNodeInspector;
  const q = studioState.selectedNode;

  if (!q || !studioState.states.includes(q)) {
    container.innerHTML = `<p style="font-size:0.8rem; color:var(--text-muted); margin:0;">Click a state circle to edit its properties.</p>`;
    return;
  }

  const isStart = (q === studioState.startState);
  let html = `
    <div style="display:flex; flex-direction:column; gap:0.6rem; font-size:0.82rem;">
      <div>
        <label style="font-weight:600; display:block; margin-bottom:2px;">State Identifier:</label>
        <div style="display:flex; gap:0.4rem;">
          <input type="text" id="inspectorNodeName" class="form-input" value="${q}" style="flex:1; padding:0.3rem 0.5rem; font-size:0.85rem;">
          <button id="btnInspectorRename" class="btn btn-secondary" style="padding:0.3rem 0.6rem; font-size:0.75rem;">Rename</button>
        </div>
      </div>

      <div style="display:flex; align-items:center; justify-content:space-between; margin-top:2px;">
        <span style="font-weight:600;">Start State:</span>
        <button id="btnInspectorToggleStart" class="btn ${isStart ? 'btn-success' : 'btn-secondary'}" style="padding:0.25rem 0.6rem; font-size:0.75rem;">
          ${isStart ? '✓ Initial State' : 'Make Initial State'}
        </button>
      </div>
  `;

  if (studioState.type === 'Moore') {
    const curOut = studioState.stateOutputs[q] || '0';
    html += `
      <div>
        <label style="font-weight:600; display:block; margin-bottom:2px;">Moore State Output λ(${q}):</label>
        <input type="text" id="inspectorStateOutput" class="form-input" value="${curOut}" maxlength="3" style="width:100%; padding:0.3rem 0.5rem; font-size:0.85rem;">
      </div>
    `;
  }

  html += `
      <div style="margin-top:0.3rem; border-top:1px solid var(--border); padding-top:0.5rem;">
        <button id="btnInspectorDeleteState" class="btn btn-secondary" style="width:100%; color:var(--danger); font-size:0.75rem; padding:0.3rem;">
          🗑️ Delete State '${q}'
        </button>
      </div>
    </div>
  `;

  container.innerHTML = html;

  // Bind inspector buttons
  document.getElementById('btnInspectorRename').addEventListener('click', () => {
    const newName = document.getElementById('inspectorNodeName').value.trim();
    if (newName && newName !== q) {
      if (studioState.states.includes(newName)) {
        alert(`State name '${newName}' already exists!`);
        return;
      }
      // Update state name everywhere
      studioState.states = studioState.states.map(s => s === q ? newName : s);
      studioState.nodePositions[newName] = studioState.nodePositions[q];
      delete studioState.nodePositions[q];

      if (studioState.stateOutputs[q] !== undefined) {
        studioState.stateOutputs[newName] = studioState.stateOutputs[q];
        delete studioState.stateOutputs[q];
      }
      if (studioState.startState === q) {
        studioState.startState = newName;
      }
      studioState.transitions.forEach(t => {
        if (t.from === q) t.from = newName;
        if (t.to === q) t.to = newName;
      });
      studioState.selectedNode = newName;
      renderStudioSvg();
      renderStudioLiveTable();
      renderStudioInspector();
    }
  });

  document.getElementById('btnInspectorToggleStart').addEventListener('click', () => {
    studioState.startState = q;
    renderStudioSvg();
    renderStudioLiveTable();
    renderStudioInspector();
  });

  if (studioState.type === 'Moore') {
    document.getElementById('inspectorStateOutput').addEventListener('input', (e) => {
      studioState.stateOutputs[q] = e.target.value.trim() || '0';
      renderStudioSvg();
      renderStudioLiveTable();
    });
  }

  document.getElementById('btnInspectorDeleteState').addEventListener('click', () => {
    studioState.states = studioState.states.filter(s => s !== q);
    delete studioState.nodePositions[q];
    delete studioState.stateOutputs[q];
    studioState.transitions = studioState.transitions.filter(t => t.from !== q && t.to !== q);
    if (studioState.startState === q) {
      studioState.startState = studioState.states[0] || '';
    }
    studioState.selectedNode = studioState.states[0] || null;
    renderStudioSvg();
    renderStudioLiveTable();
    renderStudioInspector();
  });
}

// Apply studio diagram to the workspace & run conversion
function applyStudioDiagram() {
  if (studioState.states.length === 0) {
    alert("Please add at least one state before applying.");
    return;
  }

  // Derive input alphabet from transitions
  const inputSet = new Set(studioState.transitions.map(t => t.symbol));
  if (inputSet.size === 0) {
    inputSet.add('0');
    inputSet.add('1');
  }
  const inputAlphabet = Array.from(inputSet).sort();

  // Complete any missing transitions with self-loops
  const covered = new Set(studioState.transitions.map(t => `${t.from},${t.symbol}`));
  studioState.states.forEach(q => {
    inputAlphabet.forEach(a => {
      if (!covered.has(`${q},${a}`)) {
        const fallback = { from: q, symbol: a, to: q };
        if (studioState.type === 'Mealy') {
          fallback.output = '0';
        }
        studioState.transitions.push(fallback);
      }
    });
  });

  const outputSet = new Set();
  if (studioState.type === 'Moore') {
    Object.values(studioState.stateOutputs).forEach(o => outputSet.add(o));
  } else {
    studioState.transitions.forEach(t => outputSet.add(t.output || '0'));
  }
  if (outputSet.size === 0) outputSet.add('0');
  const outputAlphabet = Array.from(outputSet).sort();

  const machineData = {
    name: `User Drawn ${studioState.type} Machine`,
    type: studioState.type,
    states: studioState.states,
    input_alphabet: inputAlphabet,
    output_alphabet: outputAlphabet,
    start_state: studioState.startState || studioState.states[0],
    transitions: studioState.transitions
  };

  if (studioState.type === 'Moore') {
    machineData.state_outputs = { ...studioState.stateOutputs };
    studioState.states.forEach(q => {
      if (!machineData.state_outputs[q]) machineData.state_outputs[q] = '0';
    });
  }

  // 1. Set source machine
  state.sourceMachine = machineData;
  state.activeSourcePresetId = null;

  // 2. Set mode without overwriting with preset!
  const targetMode = (studioState.type === 'Moore') ? 'MooreToMealy' : 'MealyToMoore';
  setMode(targetMode, false);

  // 3. Render and run conversion immediately
  renderSourceMachine();
  clearConvertedMachine();
  closeDiagramStudio();
  runConversion();
}
