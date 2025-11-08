import '@testing-library/jest-dom';

import { initialize } from '../lists.js';

describe("Superlists JavaScript", () => {
    const inputId = "id_text";
    const errorClass = "invalid-feedback";
    const inputSelector = `#${inputId}`;
    let testDiv;
    let textInput;

    beforeEach(() => {
        testDiv = document.createElement("div");
        testDiv.innerHTML = `
            <form>
                <input
                    id="${inputId}"
                    name="text"
                    class="form-control form-control-lg is-invalid"
                    placeholder="Enter a to-do item"
                    value="Value as submitted"
                    aria-describedby="id_text_feedback"
                    required
                >
                <div id="id_text_feedback" class="${errorClass}">An error message</div>
            </form>
        `;
        document.body.appendChild(testDiv);
        textInput = document.querySelector(inputSelector);
        initialize(inputSelector);
    });

    afterEach(() => {
       testDiv.remove(); 
    });

    it("should hide error message on input", async () => {
        textInput.dispatchEvent(new InputEvent("input"));
        expect(textInput).not.toHaveClass("is-invalid");
    });

    it("should not hide error message before event is fired", () => {
        expect(textInput).toHaveClass("is-invalid"); 
    });
});
