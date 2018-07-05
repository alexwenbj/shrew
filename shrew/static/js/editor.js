import CodeMirror from "codemirror-minified";
import "codemirror-minified/mode/python/python";
import "codemirror-minified/addon/edit/closebrackets";
import "codemirror-minified/addon/lint/lint";

import replaceError from "./error-replacements.js";

const textarea = document.getElementById("editor-code");

if (textarea) {
    const iframe = document.getElementById("interpreter-sandbox");
    const output = document.getElementById("code-output");
    const sandbox = iframe.contentWindow;
    let editor = CodeMirror.fromTextArea(textarea, {
        lineNumbers: true,
        theme: "shrew",
        indentUnit: 4,
        autofocus: true,
        autoCloseBrackets: true,
        lint: {
            getAnnotations: runLint,
            async: true,
        },
        gutters: ["CodeMirror-lint-markers"],
    });
    let lintCallback;
    let shrewInterpreterReady = false;

    function runCode() {
        sandbox.postMessage({code: editor.getValue()}, "*");
    }

    function runLint(text, callback) {
        if (shrewInterpreterReady) {
            runCode();
        }
        lintCallback = callback;
    }

    // run again when the tab is opened - sometimes background tab are slowed down by the browser
    // and the execution of the coee times out
    document.addEventListener("visibilitychange", () => {
        if (!document.hidden) {
            runCode();
        }
    });

    window.addEventListener("message", (event) => {
        if (event.data.type === "interpreter-ready") {
            shrewInterpreterReady = true;
            runCode();
        } else if(event.data.type === "run-result") {
            output.innerHTML = ''; // clear output
            if (event.data.out.length || event.data.error) {
                output.classList.add("has-output");
            } else {
                output.classList.remove("has-output");
            }

            for (let line of event.data.out) {
                let pre = document.createElement('pre');
                pre.innerText = line;
                output.appendChild(pre);
            }
            let errors = [];
            if (event.data.error) {
                let message = replaceError(event.data.error.message);
                let lineNumber = event.data.error.lineNumber;

                let pre = document.createElement('pre');
                pre.innerText = `${message} (line ${lineNumber})`;
                pre.classList.add("error");
                output.appendChild(pre);

                errors.push({
                    from: CodeMirror.Pos(lineNumber - 1),
                    to: CodeMirror.Pos(lineNumber - 1),
                    message: message,
                });
            }
            if (lintCallback) {
                lintCallback(errors);
            }
        }
    });
}
