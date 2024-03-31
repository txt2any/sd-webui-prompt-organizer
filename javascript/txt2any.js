const url = 'https://www.txt2any.com'
function openInT2a() {
  try {
    const detail = gradioApp().querySelector("img[data-testid='detailed-image']")
    const filename = detail.src.replace(/.*\/([^\/]+\.png).*/, '$1')
    window.open(url + '/#/cloud?filename=' + filename)
  } catch(e) {
    window.open(url + '/#/cloud')
  }
}

function createButton(id, className, onClick) {
  const button = document.createElement("button");
  button.id = id;
  button.innerHTML = "";
  button.className = className;
  const style = "width: 38px; height: 38px; max-width: 38px; max-height: 38px;"
  + "background-image: url(/file=extensions/sd-webui-prompt-organizer/images/btn.png);"
  + "background-size: contain;"
  + "background-position: center;"
  + "background-repeat: no-repeat;"
  button.style = style
  button.addEventListener("click", onClick);
  return button;
}

onUiLoaded(() => {
  const buttons = gradioApp().querySelector("#image_buttons_txt2img > .form");
  const btnCreated = gradioApp().querySelector("#open_in_t2a_btn");
  const btnOpenFolder = gradioApp().querySelector("#txt2img_open_folder");
  if (!buttons || btnCreated) return;
  const openInT2aBtn = createButton(
    "open_in_t2a_btn",
    btnOpenFolder.className,
    openInT2a
  );
  buttons.appendChild(openInT2aBtn);
})