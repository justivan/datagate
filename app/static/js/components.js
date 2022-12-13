class CustomSelect {
  init(params) {
    this.select = document.createElement("select");
    this.select.id = "custom-select";
    this.cellEditorParams = [];
    params.colDef.cellEditorParams.values.forEach((obj) =>
      this.cellEditorParams.push({
        value: obj.id,
        label: obj.name,
        selected: params.value == obj.id ? true : false,
      })
    );
  }

  getGui() {
    return this.select;
  }

  afterGuiAttached() {
    let element = document.getElementById("custom-select");
    let jsChoices = new Choices(element, {
      itemSelectText: "",
    });

    const choicesInner = document.querySelector(".choices__inner");

    let width = Math.max.apply(
      Math,
      this.cellEditorParams.map(function (el) {
        return el.label.length;
      })
    );

    choicesInner.style.minWidth =
      width * 10 > 500 ? `350px` : `${width * 10}px`;
    jsChoices.setChoices(this.cellEditorParams, "value", "label", false);

    this.select.focus();
  }

  getValue() {
    return this.select.value;
  }

  destroy() {}

  isPopup() {
    return true;
  }
}

class DiscountHeaderGroup {
  init(params) {
    this.params = params;
    this.eGui = document.createElement("div");
    this.eGui.className = "flex h-full w-full shadow-xl relative justify-center items-center";
    this.eGui.innerHTML = `
      ${this.params.displayName}
      <div>
      <input type="number" name="discount" id="discount" class="block w-full flex-1 rounded-none border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 text-xs" placeholder="www.example.com">
      </div>
    `;
  }

  getGui() {
    return this.eGui;
  }

  destroy() {}
}
