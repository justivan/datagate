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

class CheckboxRenderer {
  init(agParams) {
    this.eGui = document.createElement("div");
    this.eGui.className = "ag-cell-wrapper";

    this.inputWrapper = document.createElement("div");
    this.inputWrapper.className = "ag-selection-checkbox";

    this.input = document.createElement("input");
    this.input.type = "checkbox";
    this.input.className =
      "h-4 w-4 rounded-sm border-gray-300 text-blue-500 focus:ring-0";
    this.input.checked = agParams.value ? true : false;

    if (agParams.data.discount_pct == 0) {
      this.input.disabled = true;
      this.input.className = "hidden";
    }

    this.eGui.append(this.inputWrapper);
    this.inputWrapper.append(this.input);

    this.cellValue = document.createElement("span");
    this.cellValue.className = "ag-cell-value";
    this.cellValue.innerHTML = agParams.value;

    this.eGui.append(this.cellValue);

    this.input.onclick = () => {
      ajax("/api/booking/rate/update", {
        reserv_id: agParams.data.reserv_id,
        e_date: agParams.data.e_date,
        [agParams.colDef.field]: this.input.checked,
      }).then((response) => {
        agParams.api.forEachNode((rowNode) => {
          if (rowNode.data.e_date == agParams.data.e_date) {
            rowNode.setData(response.data[0]);
          }
        });
      });
    };
  }

  getGui() {
    return this.eGui;
  }

  destroy() {}
}

class CheckboxEditor {
  init(agParams) {
    this.agParams = agParams;
    this.eGui = document.createElement("div");
    this.eGui.className = "ag-cell-wrapper justify-center z-100";

    this.inputWrapper = document.createElement("div");
    this.inputWrapper.className = "ag-selection-checkbox";

    this.input = document.createElement("input");
    this.input.type = "checkbox";
    this.input.className =
      "h-4 w-4 rounded-sm border-gray-300 text-blue-500 focus:ring-0";

    this.eGui.append(this.inputWrapper);
    this.inputWrapper.append(this.input);

    this.input.ondblclick = () => {
      console.log(this.input.checked);
      // params.field.forEach((element) => {
      //   console.log(params.field)
      //   let value = this.input.checked
      //     ? params.data[element] * (params.data.discount_pct / 100) * -1
      //     : 0;
      //   console.log(value);
      //   ajax("/api/booking/rate/update", {
      //     reserv_id: params.data.reserv_id,
      //     e_date: params.data.e_date,
      //     [element.concat("_discount")]: value,
      //   }).then((response) => {
      //     params.api.forEachNode((rowNode) => {
      //       if (rowNode.data.e_date == params.data.e_date) {
      //         rowNode.setData(response.data[0]);
      //       }
      //     });
      //   });
      // });
    };
  }

  getGui() {
    return this.eGui;
  }

  afterGuiAttached() {
    this.eGui.focus();
  }

  getValue() {
    return this.eGui.value;
  }

  destroy() {}

  isPopup() {}
}
