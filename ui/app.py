"""
CEPAC Web UI - Flask Application

A web interface for configuring and running the CEPAC HIV/AIDS simulation model.
"""

import os
import json
import sys
from flask import Flask, render_template, request, jsonify, send_file, Response
from io import BytesIO

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from param_schema import create_default_params, get_param_metadata, CONSTANTS
from input_parser import parse_in_content
from input_generator import generate_in_file
from model_runner import ModelRunner

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cepac-ui-secret-key'

# Global state for current parameters
current_params = create_default_params()


@app.route('/')
def index():
    """Render the main UI page."""
    metadata = get_param_metadata()
    return render_template('index.html',
                         tabs=metadata['tabs'],
                         constants=CONSTANTS)


@app.route('/api/params', methods=['GET'])
def get_params():
    """Get current parameter values."""
    return jsonify(current_params)


@app.route('/api/params', methods=['POST'])
def set_params():
    """Update parameter values."""
    global current_params
    data = request.get_json()

    if data:
        # Merge updates into current params
        for tab, values in data.items():
            if tab in current_params:
                if isinstance(values, dict):
                    current_params[tab].update(values)
                else:
                    current_params[tab] = values

    return jsonify({'success': True, 'message': 'Parameters updated'})


@app.route('/api/params/reset', methods=['POST'])
def reset_params():
    """Reset parameters to defaults."""
    global current_params
    current_params = create_default_params()
    return jsonify({'success': True, 'message': 'Parameters reset to defaults'})


@app.route('/api/export', methods=['GET'])
def export_in_file():
    """Export current parameters as .in file."""
    content = generate_in_file(current_params)

    # Create file-like object for download
    buffer = BytesIO(content.encode('utf-8'))
    buffer.seek(0)

    run_name = current_params.get('runspecs', {}).get('runName', 'cepac_run')
    filename = f'{run_name}.in'

    return send_file(
        buffer,
        mimetype='text/plain',
        as_attachment=True,
        download_name=filename
    )


@app.route('/api/import', methods=['POST'])
def import_in_file():
    """Import parameters from .in file."""
    global current_params

    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'}), 400

    try:
        content = file.read().decode('utf-8')
        current_params = parse_in_content(content)
        return jsonify({
            'success': True,
            'message': f'Imported {file.filename}',
            'params': current_params
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error parsing file: {str(e)}'
        }), 400


@app.route('/api/run', methods=['POST'])
def run_model():
    """Run the CEPAC model with current parameters."""
    try:
        # Generate input file
        input_content = generate_in_file(current_params)
        run_name = current_params.get('runspecs', {}).get('runName', 'uirun')

        # Run the model
        runner = ModelRunner()
        result = runner.run(input_content, run_name)

        return jsonify(result)

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error running model: {str(e)}'
        }), 500


@app.route('/api/compile', methods=['POST'])
def compile_model():
    """Compile the CEPAC model."""
    try:
        runner = ModelRunner()
        success, message = runner.compile()
        return jsonify({'success': success, 'message': message})
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error compiling: {str(e)}'
        }), 500


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get model runner status."""
    runner = ModelRunner()
    return jsonify(runner.get_status())


@app.route('/api/metadata', methods=['GET'])
def get_metadata():
    """Get parameter metadata for UI generation."""
    return jsonify(get_param_metadata())


@app.route('/api/constants', methods=['GET'])
def get_constants():
    """Get model constants."""
    return jsonify(CONSTANTS)


@app.route('/api/validate', methods=['POST'])
def validate_params():
    """Validate current parameters."""
    errors = []
    warnings = []

    p = current_params

    # Basic validation
    runspecs = p.get('runspecs', {})
    if runspecs.get('numCohorts', 0) <= 0:
        errors.append('Cohort size must be positive')

    if runspecs.get('discountFactor', 0) < 0:
        errors.append('Discount factor cannot be negative')

    cohort = p.get('cohort', {})
    if cohort.get('initialCD4Mean', 0) <= 0:
        errors.append('Initial CD4 mean must be positive')

    if cohort.get('maleGenderDistribution', 0) < 0 or cohort.get('maleGenderDistribution', 1) > 1:
        errors.append('Male gender distribution must be between 0 and 1')

    # Warnings for common issues
    if runspecs.get('numCohorts', 0) < 1000:
        warnings.append('Small cohort size may give unstable results')

    return jsonify({
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings
    })


# Tab-specific routes for rendering tab content
@app.route('/tab/<tab_id>')
def render_tab(tab_id):
    """Render a specific tab's content."""
    template_map = {
        'runspecs': 'tabs/runspecs.html',
        'output': 'tabs/output.html',
        'cohort': 'tabs/cohort.html',
        'treatment': 'tabs/treatment.html',
        'ltfu': 'tabs/ltfu.html',
        'heterogeneity': 'tabs/heterogeneity.html',
        'sti': 'tabs/sti.html',
        'prophs': 'tabs/prophs.html',
        'arts': 'tabs/arts.html',
        'nathist': 'tabs/nathist.html',
        'chrms': 'tabs/chrms.html',
        'costs': 'tabs/costs.html',
        'tb': 'tabs/tb.html',
        'qol': 'tabs/qol.html',
        'hivtest': 'tabs/hivtest.html',
        'peds': 'tabs/peds.html',
        'pedsarts': 'tabs/pedsarts.html',
        'pedscosts': 'tabs/pedscosts.html',
        'eid': 'tabs/eid.html',
        'adolescent': 'tabs/adolescent.html',
        'adolescentarts': 'tabs/adolescentarts.html',
        'results': 'tabs/results.html',
    }

    template = template_map.get(tab_id, 'tabs/generic.html')
    params = current_params.get(tab_id, {})

    return render_template(template,
                         tab_id=tab_id,
                         params=params,
                         constants=CONSTANTS)


# Output file download endpoints
PRESETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'presets')


@app.route('/api/outputs', methods=['GET'])
def list_outputs():
    """List available output files in presets directory."""
    outputs = []
    if os.path.exists(PRESETS_DIR):
        for filename in sorted(os.listdir(PRESETS_DIR)):
            if filename.endswith('.out'):
                filepath = os.path.join(PRESETS_DIR, filename)
                outputs.append({
                    'filename': filename,
                    'size': os.path.getsize(filepath),
                    'modified': os.path.getmtime(filepath)
                })
    return jsonify({'outputs': outputs})


@app.route('/api/outputs/<filename>', methods=['GET'])
def download_output(filename):
    """Download a specific output file."""
    # Security: only allow .out files and prevent directory traversal
    if not filename.endswith('.out') or '/' in filename or '\\' in filename:
        return jsonify({'error': 'Invalid filename'}), 400

    filepath = os.path.join(PRESETS_DIR, filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404

    return send_file(
        filepath,
        mimetype='text/plain',
        as_attachment=True,
        download_name=filename
    )


@app.route('/api/outputs/<filename>/preview', methods=['GET'])
def preview_output(filename):
    """Preview content of an output file."""
    if not filename.endswith('.out') or '/' in filename or '\\' in filename:
        return jsonify({'error': 'Invalid filename'}), 400

    filepath = os.path.join(PRESETS_DIR, filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404

    try:
        with open(filepath, 'r') as f:
            content = f.read()
        return jsonify({'filename': filename, 'content': content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='CEPAC Web UI')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to listen on')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')

    args = parser.parse_args()

    print(f"Starting CEPAC UI at http://{args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=args.debug)
