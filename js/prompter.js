import { app } from "../../scripts/app.js";
import { ComfyWidgets } from "../../../scripts/widgets.js"

app.registerExtension({
    name: "prompt.preview",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeType.comfyClass === "PlaceholderPrompting") {
            nodeType.prototype.onNodeCreated = function() {
                this.addInput("input_string", "STRING");
                this.showValueWidget = ComfyWidgets["STRING"](this, "preview", ["STRING", { multiline: true }], app).widget;
                this.showValueWidget.inputEl.readOnly = true;
                this.showValueWidget.inputEl.style.opacity = 0.7;
            };

            const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function(message) {
                onExecuted?.apply(this, arguments);
                if (message?.text?.[0] !== undefined) {
                    this.showValueWidget.value = message.text[0];
                }
            };
        }
    }
});
