# C-PAC pre-commit examples

This repository shows examples of the ["Existing code needs linting" strategy options](https://docs.google.com/document/d/1WmKICJAMSIUlsFmUFgvbD-Ev9YmTQ9B9xPGbjVpxi8c/edit#heading=h.6osuppnfw5c9) for [:octocat:/FCP-INDI/C-PAC](https://github.com/FCP-INDI/C-PAC).

An interactive visualization of the shape of the branches from each option can be found [in the Insights tab, in the Network graph](https://github.com/childmindresearch/C-PAC_pre-commit_examples/network).

## Comparison of options

<table>
  <tr>
    <th colspan="2" rowspan="2">Option</th>
    <th colspan="2">Review</th>
    <th rowspan="2">ruff</th>
  </tr>
  <tr>
    <th>style</th>
    <th>code</th>
  </tr>
  <tr>
    <th rowspan="2"><a href="https://docs.google.com/document/d/1WmKICJAMSIUlsFmUFgvbD-Ev9YmTQ9B9xPGbjVpxi8c/edit#heading=h.mxkde4td2if3">1: double branching</a></th>
    <th>without a rebase</th>
    <td><a href="https://github.com/childmindresearch/C-PAC_pre-commit_examples/compare/174f5cb...7e96298"><img src="./assets/screenshots/diff_option-1_style.png" alt="174f5cb...7e96298"></a></td>
    <td><a href="https://github.com/childmindresearch/C-PAC_pre-commit_examples/compare/7e96298...6039154"><img src="./assets/screenshots/diff_option-1_code.png" alt="7e96298...6039154"></a></td>
    <td rowspan="2">
<pre>
ruff.....................................................................Passed</pre>
    </td>
  </tr>
  <tr>
  <th>with a rebase<a href="#rebase-note" name="rebase-note-1" id="rebase-note-1"><sup>*</sup></a></th>
    <td><a href="https://github.com/childmindresearch/C-PAC_pre-commit_examples/compare/174f5cb...20d1573"><img src="./assets/screenshots/diff_option-1-with-rebase_style.png" alt="174f5cb...20d1573"></a></td>
    <td><a href="https://github.com/childmindresearch/C-PAC_pre-commit_examples/compare/20d1573...a7aba9e"><img src="./assets/screenshots/diff_option-1-with-rebase_code.png" alt="20d1573...a7aba9e"></a></td>
  </tr>
  <tr>
    <th colspan="2"><a href="https://docs.google.com/document/d/1WmKICJAMSIUlsFmUFgvbD-Ev9YmTQ9B9xPGbjVpxi8c/edit#heading=h.mzkv8tw4zpcl">2: make changes in a different file</a></th>
    <td colspan="2"><a href="https://github.com/childmindresearch/C-PAC_pre-commit_examples/compare/174f5cb...a8bfcef"><img src="./assets/screenshots/diff_option-2.png" alt="174f5cb...a8bfcef"></a></td>
    <td>
<pre>
ruff.....................................................................Failed
- hook id: ruff
- exit code: 1

CPAC/qc/xcp.py:1:1: D400 First line should end with a period
CPAC/qc/xcp.py:155:5: D401 First line of docstring should be in imperative mood: "Function to correlate DVARS and FD-J."
CPAC/qc/xcp.py:168:5: D401 First line of docstring should be in imperative mood: "Function to gather BIDS information from a strat_pool."
CPAC/qc/xcp.py:272:5: D103 Missing docstring in public function
Found 4 errors.
</pre>
    </td>
  </tr>
  <tr>
    <th colspan="2"><a href="https://docs.google.com/document/d/1WmKICJAMSIUlsFmUFgvbD-Ev9YmTQ9B9xPGbjVpxi8c/edit#heading=h.w674v857o0lw">3: lint and make changes all in one branch</a></th>
    <td colspan="2"><a href="https://github.com/childmindresearch/C-PAC_pre-commit_examples/compare/174f5cb...9fc86e0"><img src="./assets/screenshots/diff_option-3.png" alt="174f5cb...9fc86e0"></a></td>
    <td>
<pre>
ruff.....................................................................Passed
</pre>
    </td>
  </tr>
  <tr>
    <th colspan="2"><a href="https://docs.google.com/document/d/1WmKICJAMSIUlsFmUFgvbD-Ev9YmTQ9B9xPGbjVpxi8c/edit#heading=h.wgr4mef1nd6w">4: ignore violations outside of your changes</a></th>
    <td></td><td><a href="https://github.com/childmindresearch/C-PAC_pre-commit_examples/compare/174f5cb...e3bea9f"><img src="./assets/screenshots/diff_option-4.png" alt="174f5cb...e3bea9f"></a></td>
    <td>
<pre>
ruff.....................................................................Failed
- hook id: ruff
- exit code: 1

CPAC/qc/xcp.py:1:1: D400 First line should end with a period
CPAC/qc/xcp.py:161:5: D401 First line of docstring should be in imperative mood: "Function to correlate DVARS and FD-J."
CPAC/qc/xcp.py:173:5: PLR0913 Too many arguments in function definition (18 > 10)
CPAC/qc/xcp.py:194:5: D401 First line of docstring should be in imperative mood: "Function to generate an RBC-style QC CSV."
CPAC/qc/xcp.py:347:5: D401 First line of docstring should be in imperative mood: "Function to gather BIDS information from a strat_pool."
CPAC/qc/xcp.py:451:5: D103 Missing docstring in public function
Found 6 errors.
</pre>
    </td>
  </tr>
</table>

<a href="#rebase-note-1" name="rebase-note" id="rebase-note"><sup>*</sup></a> The rebase example includes linting one more file than the other examples.
