export const initialize = (inputSelector) => {
    const textInput = document.querySelector("#id_text");
    textInput.oninput = () => {
        textInput.classList.remove("is-invalid");
    }
};
