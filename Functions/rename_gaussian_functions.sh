#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="${1:-.}"
MODE="${2:-dry-run}"

if [[ "$MODE" != "dry-run" && "$MODE" != "--apply" ]]; then
    echo "Usage:"
    echo "  bash rename_gaussian_functions.sh /path/to/repo"
    echo "  bash rename_gaussian_functions.sh /path/to/repo --apply"
    exit 1
fi

cd "$REPO_DIR"

if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo "ERROR: This does not look like a git repository:"
    echo "  $REPO_DIR"
    exit 1
fi

echo "Repository:"
git rev-parse --show-toplevel
echo ""

if [[ "$MODE" == "dry-run" ]]; then
    echo "Running in dry-run mode. No files will be modified."
else
    echo "Running in APPLY mode. Files will be modified."
fi

echo ""

MAPPING_FILE="$(mktemp)"

cat > "$MAPPING_FILE" <<'EOF'
AdjacencyClustering adjacency_clustering
ChromGaussPeak chrom_gauss_peak
SignalsModulesStats signals_modules_stats
CloseNeighboursList close_neighbours_list
WeightGauss weight_gauss
BiggestSelector biggest_selector
r2_Model r2_model
OverlappingGaussPeaks overlapping_gauss_peaks
LowSignalClustering low_signal_clustering
UpdatingChromMat updating_chrom_mat
RefineChromMat refine_chrom_mat
ParametersFitGaussParallelPeaks parameters_fit_gauss_parallel_peaks
AdjustingPeaksContributions adjusting_peaks_contributions
Mate_square_GaussParPop mate_square_gauss_par_pop
FitnessSelector fitness_selector
EvaluatePopulation evaluate_population
RedistributeSampling redistribute_sampling
CuttingFreq cutting_freq
RefineChromPeak refine_chrom_peak
Mate_Generations mate_generations
SmoothSavgol smooth_savgol
SmoothFourier smooth_fourier
UmbrellasStats umbrellas_stats
RefinePop_OnePeak refine_pop_one_peak
SmoothData_and_FindPeaks smooth_data_and_find_peaks
RawGaussSeed raw_gauss_seed
GaussBoundaries gauss_boundaries
ToolsGaussianChrom tools_gaussian_chrom
ShowDF show_df
GaussianChromatogram gaussian_chromatogram
ResolvingGaussianChromatogram resolving_gaussian_chromatogram
ResolveFullChromatogram resolve_full_chromatogram
EOF

echo "Planned function/module renames:"
column -t "$MAPPING_FILE"
echo ""

echo "Checking current git status..."
git status --short
echo ""

if [[ "$MODE" == "--apply" ]]; then
    echo "Creating safety branch..."
    BRANCH_NAME="rename-gaussian-functions-$(date +%Y%m%d-%H%M%S)"
    git switch -c "$BRANCH_NAME"
    echo "Created branch: $BRANCH_NAME"
    echo ""
fi

echo "Renaming .py files if their names match old function names..."

while read -r OLD_NAME NEW_NAME; do
    OLD_FILE="${OLD_NAME}.py"
    NEW_FILE="${NEW_NAME}.py"

    while IFS= read -r FILE_PATH; do
        [[ -z "$FILE_PATH" ]] && continue

        DIR_NAME="$(dirname "$FILE_PATH")"
        TARGET_PATH="${DIR_NAME}/${NEW_FILE}"

        if [[ "$FILE_PATH" == "$TARGET_PATH" ]]; then
            continue
        fi

        if [[ -e "$TARGET_PATH" ]]; then
            echo "SKIP: target already exists:"
            echo "  $TARGET_PATH"
            continue
        fi

        if [[ "$MODE" == "--apply" ]]; then
            if git ls-files --error-unmatch "$FILE_PATH" > /dev/null 2>&1; then
                git mv "$FILE_PATH" "$TARGET_PATH"
            else
                mv "$FILE_PATH" "$TARGET_PATH"
            fi
            echo "RENAMED: $FILE_PATH -> $TARGET_PATH"
        else
            echo "WOULD RENAME: $FILE_PATH -> $TARGET_PATH"
        fi

    done < <(git ls-files -co --exclude-standard -- "**/${OLD_FILE}" "${OLD_FILE}" 2>/dev/null || true)

done < "$MAPPING_FILE"

echo ""
echo "Updating Python identifier names inside .py files..."

PYTHON_SCRIPT="$(mktemp).py"

cat > "$PYTHON_SCRIPT" <<'PY'
from __future__ import annotations

import io
import pathlib
import sys
import tokenize


def read_mapping(mapping_file):
    mapping = {}

    with open(mapping_file, "r", encoding="utf-8") as file_obj:
        for line in file_obj:
            line = line.strip()

            if not line:
                continue

            old_name, new_name = line.split()
            mapping[old_name] = new_name

    return mapping


def replace_python_names(source_text,
                         mapping):
    tokens = []
    changed = False

    reader = io.StringIO(source_text).readline

    for token in tokenize.generate_tokens(reader):
        token_type = token.type
        token_string = token.string

        if token_type == tokenize.NAME and token_string in mapping:
            token = tokenize.TokenInfo(type=token.type,
                                       string=mapping[token_string],
                                       start=token.start,
                                       end=token.end,
                                       line=token.line)

            changed = True

        tokens.append(token)

    new_text = tokenize.untokenize(tokens)

    return new_text, changed


def main():
    mapping_file = pathlib.Path(sys.argv[1])
    apply_changes = sys.argv[2] == "--apply"
    py_files = [pathlib.Path(path) for path in sys.argv[3:]]

    mapping = read_mapping(mapping_file)

    changed_files = []

    for py_file in py_files:
        if not py_file.exists():
            continue

        source_text = py_file.read_text(encoding="utf-8")
        new_text, changed = replace_python_names(source_text=source_text,
                                                 mapping=mapping)

        if changed:
            changed_files.append(str(py_file))

            if apply_changes:
                py_file.write_text(new_text,
                                   encoding="utf-8")

    for changed_file in changed_files:
        if apply_changes:
            print(f"UPDATED: {changed_file}")
        else:
            print(f"WOULD UPDATE: {changed_file}")


if __name__ == "__main__":
    main()
PY

mapfile -t PY_FILES < <(git ls-files -co --exclude-standard '*.py')

if [[ "${#PY_FILES[@]}" -eq 0 ]]; then
    echo "No Python files found."
else
    python "$PYTHON_SCRIPT" "$MAPPING_FILE" "$MODE" "${PY_FILES[@]}"
fi

echo ""
echo "Running syntax check..."

SYNTAX_SCRIPT="$(mktemp).py"

cat > "$SYNTAX_SCRIPT" <<'PY'
from __future__ import annotations

import pathlib
import py_compile
import sys


failed_files = []

for file_path in sys.argv[1:]:
    path = pathlib.Path(file_path)

    if not path.exists():
        continue

    try:
        py_compile.compile(str(path),
                           doraise=True)

    except Exception as error:
        failed_files.append((str(path), str(error)))

if failed_files:
    print("Syntax check failed:")
    for file_path, error in failed_files:
        print("")
        print(file_path)
        print(error)
    sys.exit(1)

print("Syntax check passed.")
PY

if [[ "$MODE" == "--apply" ]]; then
    mapfile -t PY_FILES_AFTER < <(git ls-files -co --exclude-standard '*.py')
    python "$SYNTAX_SCRIPT" "${PY_FILES_AFTER[@]}"
else
    echo "Skipped in dry-run mode."
fi

echo ""
echo "Final git status:"
git status --short

echo ""
if [[ "$MODE" == "dry-run" ]]; then
    echo "Dry-run complete. Re-run with --apply to make changes."
else
    echo "Rename complete."
    echo "Review with:"
    echo "  git diff"
fi
