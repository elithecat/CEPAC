"""
CEPAC Model Runner

Compiles and executes the CEPAC model, capturing output.
"""

import os
import subprocess
import tempfile
import shutil
from pathlib import Path


class ModelRunner:
    """Runs the CEPAC simulation model."""

    def __init__(self, cepac_dir=None):
        """Initialize with path to CEPAC source directory."""
        if cepac_dir is None:
            # Default to parent of ui directory
            cepac_dir = Path(__file__).parent.parent
        self.cepac_dir = Path(cepac_dir)
        self.executable = self.cepac_dir / 'cepac'

    def compile_if_needed(self):
        """Compile the CEPAC model if executable doesn't exist or is outdated."""
        if self.executable.exists():
            # Check if any source file is newer than executable
            exe_mtime = self.executable.stat().st_mtime
            needs_recompile = False

            for src in self.cepac_dir.glob('*.cpp'):
                if src.stat().st_mtime > exe_mtime:
                    needs_recompile = True
                    break

            for hdr in self.cepac_dir.glob('*.h'):
                if hdr.stat().st_mtime > exe_mtime:
                    needs_recompile = True
                    break

            if not needs_recompile:
                return True, "Executable is up to date"

        return self.compile()

    def compile(self):
        """Compile the CEPAC model."""
        try:
            cmd = [
                'g++',
                '-o', str(self.executable),
                '-std=c++11',
                '-O3',
            ] + [str(f) for f in self.cepac_dir.glob('*.cpp')]

            result = subprocess.run(
                cmd,
                cwd=str(self.cepac_dir),
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode != 0:
                return False, f"Compilation failed:\n{result.stderr}"

            return True, "Compilation successful"

        except subprocess.TimeoutExpired:
            return False, "Compilation timed out"
        except Exception as e:
            return False, f"Compilation error: {str(e)}"

    def run(self, input_file_content, run_name='uirun'):
        """
        Run the CEPAC model with given input.

        Args:
            input_file_content: Content of the .in file as string
            run_name: Name for the run (used for file naming)

        Returns:
            dict with keys: success, message, output, cout, popstats, trace
        """
        result = {
            'success': False,
            'message': '',
            'output': '',
            'cout': '',
            'popstats': '',
            'trace': '',
        }

        # Ensure compiled
        compile_ok, compile_msg = self.compile_if_needed()
        if not compile_ok:
            result['message'] = compile_msg
            return result

        # Create temporary directory for run
        with tempfile.TemporaryDirectory(prefix='cepac_') as tmpdir:
            tmpdir = Path(tmpdir)

            # Write input file
            input_path = tmpdir / f'{run_name}.in'
            with open(input_path, 'w') as f:
                f.write(input_file_content)

            try:
                # Run CEPAC
                cmd = [str(self.executable), str(tmpdir)]
                proc_result = subprocess.run(
                    cmd,
                    cwd=str(self.cepac_dir),
                    capture_output=True,
                    text=True,
                    timeout=600  # 10 minute timeout
                )

                result['message'] = proc_result.stdout
                if proc_result.returncode != 0:
                    result['message'] += f"\n\nStderr:\n{proc_result.stderr}"
                    result['success'] = False
                    return result

                # Read output files - CEPAC puts them in results/ subdirectory or root
                results_dir = tmpdir / 'results'

                # Check both locations for output files
                out_file = results_dir / f'{run_name}.out' if results_dir.exists() else tmpdir / f'{run_name}.out'
                if not out_file.exists():
                    out_file = tmpdir / f'{run_name}.out'
                if out_file.exists():
                    with open(out_file, 'r') as f:
                        result['output'] = f.read()

                cout_file = results_dir / f'{run_name}.cout' if results_dir.exists() else tmpdir / f'{run_name}.cout'
                if not cout_file.exists():
                    cout_file = tmpdir / f'{run_name}.cout'
                if cout_file.exists():
                    with open(cout_file, 'r') as f:
                        result['cout'] = f.read()

                popstats_file = results_dir / 'popstats.out' if results_dir.exists() else tmpdir / 'popstats.out'
                if not popstats_file.exists():
                    popstats_file = tmpdir / 'popstats.out'
                if popstats_file.exists():
                    with open(popstats_file, 'r') as f:
                        result['popstats'] = f.read()

                # Look for trace files in both locations
                search_dirs = [tmpdir, results_dir] if results_dir.exists() else [tmpdir]
                for search_dir in search_dirs:
                    for trace_file in search_dir.glob('*.trace'):
                        with open(trace_file, 'r') as f:
                            result['trace'] += f"=== {trace_file.name} ===\n{f.read()}\n"

                result['success'] = True

            except subprocess.TimeoutExpired:
                result['message'] = "Model execution timed out (10 minute limit)"
            except Exception as e:
                result['message'] = f"Execution error: {str(e)}"

        return result

    def get_status(self):
        """Get status of the model runner."""
        status = {
            'cepac_dir': str(self.cepac_dir),
            'executable_exists': self.executable.exists(),
            'source_files': len(list(self.cepac_dir.glob('*.cpp'))),
            'header_files': len(list(self.cepac_dir.glob('*.h'))),
        }

        if self.executable.exists():
            status['executable_size'] = self.executable.stat().st_size
            status['executable_mtime'] = self.executable.stat().st_mtime

        return status


def run_model(input_content, run_name='uirun'):
    """Convenience function to run the model."""
    runner = ModelRunner()
    return runner.run(input_content, run_name)


if __name__ == '__main__':
    # Test compilation
    runner = ModelRunner()
    print("Status:", runner.get_status())

    ok, msg = runner.compile_if_needed()
    print(f"Compile: {ok}, {msg}")
