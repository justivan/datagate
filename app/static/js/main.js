async function ajax(url = "", data = {}) {
  const response = await fetch(url, {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  return response.json();
}

function getMargin(params) {
  let sales = params.data.operator_price;
  let cost = params.data.purchase;
  let margin = (((sales - cost) / cost) * 100).toFixed(2);

  return margin;
}

function getMarginCellRule(params) {
  let operator = params.data.operator_id;
  let value = params.value;
  let youtravel = [905, 1015, 1519];

  switch (true) {
    case !isFinite(value):
      return true;
      break;
    case isNaN(value):
      return true;
      break;
    case youtravel.includes(operator) && value < -5.01:
      return true;
      break;
    case value < 0 && !youtravel.includes(operator):
      return true;
      break;
    case value > 1:
      return true;
      break;
  }
}

function getDifference(params) {
  let operator_price = params.data.operator_price;
  let sales = params.data.sales;
  let difference = operator_price - sales;

  return difference.toFixed(2);
}

function loadRefData(index, data) {
  let colDefs = RESERV_GRID_OPTS.api.getColumnDefs();
  let mapping = Object.assign(
    {},
    ...data.map((obj) => ({ [obj.id]: obj.name }))
  );
  colDefs[index].cellEditorParams = { values: data };
  colDefs[index].refData = mapping;
  RESERV_GRID_OPTS.api.setColumnDefs(colDefs);
}

function getRowId(params) {
  return params.data.id;
}

function getContextMenuItems(params) {
  return [
    {
      name: "Manual Calculation",
      action: () => {
        ajax("/api/booking/rate", { id: params.node.data.id }).then(
          (response) => {
            params.api.refreshServerSide();
          }
        );
      },
      icon: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-calculator" viewBox="0 0 16 16">
      <path d="M12 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h8zM4 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H4z"/>
      <path d="M4 2.5a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-.5.5h-7a.5.5 0 0 1-.5-.5v-2zm0 4a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1zm0 3a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1zm0 3a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1zm3-6a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1zm0 3a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1zm0 3a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1zm3-6a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1zm0 3a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v4a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-4z"/>
    </svg>`,
    },
    "separator",
    "copy",
    "copyWithHeaders",
    "separator",
    "export",
  ];
}

function getRowHeight(params) {
  if (params.node && params.node.detail) {
    let offset = 60;
    let sizes = params.api.getSizesForCurrentTheme() || {};
    let allDetailRowHeight = params.data.rates.length * sizes.rowHeight + 65;
    return allDetailRowHeight + (sizes.headerHeight || 0) + offset;
  }
}

function isRowMaster(dataItem) {
  return dataItem ? dataItem.rates.length > 0 : false;
}

function getDetailRowData(params) {
  return params.successCallback(params.data.rates);
}

function detailGridUpdate(params) {
  ajax("/api/booking/rate/update", {
    reserv_id: params.data.reserv_id,
    e_date: params.data.e_date,
    [params.colDef.field]: params.newValue ? params.newValue : 0,
  }).then((response) => {
    params.api.forEachNode((rowNode) => {
      if (rowNode.data.e_date == params.data.e_date) {
        rowNode.setData(response.data[0]);
      }
    });
  });
}
const COLUMN_TYPES = {
  dateColumn: {
    valueFormatter: (params) => {
      if (params.value != null) {
        return new Date(params.value).toLocaleDateString("en-GB");
      }
    },
    filter: "agDateColumnFilter",
    filterParams: {
      filterOptions: ["equals", "lessThan", "greaterThan", "inRange"],
    },
  },
  numberColumn: {
    valueFormatter: (params) => {
      if (params.value !== null) {
        return parseFloat(params.value).toFixed(2);
      }
    },
    cellClass: "text-center",
    filter: "agNumberColumnFilter",
    filterParams: {
      filterOptions: [
        "equals",
        "notEqual",
        "lessThan",
        "lessThanOrEqual",
        "greaterThan",
        "greaterThanOrEqual",
        "inRange",
      ],
    },
  },
};

const RESERV_COLDEFS = [
  {
    headerName: "Status",
    field: "status_id",
    width: 90,
    pinned: "left",
    editable: true,
    cellEditor: CustomSelect,
    cellEditorParams: {
      values: [],
    },
    refData: {},
  },
  {
    headerName: "RefID",
    field: "gwg_ref_id",
    width: 90,
    pinned: "left",
    cellRenderer: "agGroupCellRenderer",
  },
  {
    headerName: "ResID",
    field: "gwg_res_id",
    width: 70,
    pinned: "left",
    //   cellRenderer: renderResID,
  },
  {
    headerName: "Voucher",
    field: "bkg_ref",
    width: 90,
    pinned: "left",
  },
  {
    headerName: "OprCode",
    field: "operator_code",
    width: 80,
  },
  {
    headerName: "Operator",
    field: "operator_id",
    width: 80,
    refData: {},
  },
  {
    headerName: "HotelName",
    field: "hotel_id",
    width: 180,
    editable: true,
    cellEditor: CustomSelect,
    cellEditorParams: {
      values: [],
    },
    refData: {},
  },
  {
    headerName: "ImportDate",
    field: "import_date",
    width: 90,
    type: "dateColumn",
    hide: true,
  },
  {
    headerName: "SalesDate",
    field: "sales_date",
    width: 90,
    type: "dateColumn",
  },
  {
    headerName: "InDate",
    field: "in_date",
    width: 95,
    type: "dateColumn",
    // cellEditor: DatePicker,
  },
  {
    headerName: "OutDate",
    field: "out_date",
    width: 95,
    type: "dateColumn",
    // cellEditor: DatePicker,
  },
  {
    headerName: "RoomType",
    field: "room",
    width: 130,
  },
  {
    field: "meal",
    width: 60,
    cellClass: "text-center",
  },
  {
    field: "days",
    width: 60,
    cellClass: "text-center",
  },
  {
    field: "adult",
    width: 60,
    cellClass: "text-center",
  },
  {
    field: "child",
    width: 60,
    cellClass: "text-center",
  },
  {
    field: "purchase",
    width: 80,
    type: "numberColumn",
    cellClassRules: {
      "bg-rose-400": (params) => params.value <= 0,
    },
    editable: true,
  },
  {
    field: "sales",
    width: 80,
    type: "numberColumn",
    cellClassRules: {
      "bg-rose-400": (params) => params.value <= 0,
    },
    editable: true,
  },
  {
    headerName: "OperatorPrice",
    field: "operator_price",
    width: 110,
    type: "numberColumn",
    cellClassRules: {
      "bg-rose-400": (params) => params.value <= 0,
    },
    editable: true,
  },
  {
    headerName: "Difference",
    valueGetter: getDifference,
    colId: "difference",
    width: 90,
    type: "numberColumn",
    cellClassRules: {
      "bg-rose-400": (params) => params.value < -5,
      "bg-emerald-400": (params) => params.value > 5,
    },
  },
  {
    headerName: "Margin %",
    valueGetter: getMargin,
    colId: "margin",
    width: 80,
    type: "numberColumn",
    cellClassRules: {
      "bg-rose-400": getMarginCellRule,
    },
  },
  {
    headerName: "PurchaseID",
    field: "gwg_purchase_id",
    width: 100,
    cellClass: "text-center",
  },
  {
    headerName: "PurchaseCode",
    field: "gwg_purchase_code",
    width: 150,
    cellClassRules: {
      "bg-rose-400": (params) => params.value == "-",
    },
  },
  {
    headerName: "SalesID",
    field: "gwg_sales_id",
    width: 100,
    cellClass: "text-center",
  },
  {
    headerName: "SalesCode",
    field: "gwg_sales_code",
    width: 150,
    cellClassRules: {
      "bg-rose-400": (params) => params.value == "-",
    },
  },
];

const RESERV_GRID_OPTS = {
  columnDefs: RESERV_COLDEFS,
  columnTypes: COLUMN_TYPES,
  rowModelType: "serverSide",
  serverSideInfiniteScroll: true,
  getRowId: getRowId,
  getContextMenuItems: getContextMenuItems,
  masterDetail: true,
  getRowHeight: getRowHeight,
  isRowMaster: isRowMaster,
  detailCellRendererParams: {
    getDetailRowData: getDetailRowData,
    refreshStrategy: "rows",
    detailGridOptions: {
      enableRangeSelection: true,
      enableFillHandle: true,
      onCellValueChanged: detailGridUpdate,
      onCellKeyDown: (agParams) => {
        if(agParams.event.ctrlKey && agParams.event.keyCode == 68) {
          console.log(agParams)
        }
      },
      columnTypes: COLUMN_TYPES,
      columnDefs: [
        {
          headerName: "Date",
          field: "e_date",
          width: 80,
          type: "dateColumn",
          editable: false,
          cellClass:
            "text-right !border-y-0 !border-l-0 !border-r !border-gray-200",
        },
        {
          headerName: "Rate",
          field: "base_rate",
          width: 70,
          type: "numberColumn",
          editable: true,
          cellClass:
            "text-right !border-y-0 !border-l-0 !border-r !border-gray-200",
        },
        {
          headerName: "Adult Supp",
          field: "adult_supp",
          width: 72,
          type: "numberColumn",
          cellClass:
            "text-right !border-y-0 !border-l-0 !border-r !border-gray-200",
        },
        {
          headerName: "Child Supp",
          field: "child_supp",
          width: 70,
          type: "numberColumn",
          cellClass:
            "text-right !border-y-0 !border-l-0 !border-r !border-gray-200",
        },
        {
          headerName: "Adult Meal",
          field: "adult_meal",
          width: 70,
          type: "numberColumn",
          cellClass:
            "text-right !border-y-0 !border-l-0 !border-r !border-gray-200",
        },
        {
          headerName: "Child Meal",
          field: "child_meal",
          width: 70,
          type: "numberColumn",
          cellClass:
            "text-right !border-y-0 !border-l-0 !border-r !border-gray-200",
        },
        {
          headerName: "Peak Supp",
          field: "peak_supp",
          width: 70,
          type: "numberColumn",
          cellClass:
            "text-right !border-y-0 !border-l-0 !border-r !border-gray-200",
        },
        {
          field: "extras",
          width: 70,
          type: "numberColumn",
          cellClass:
            "text-right !border-y-0 !border-l-0 !border-r !border-gray-200",
        },
        {
          headerName: "",
          // headerGroupComponent: DiscountHeaderGroup,
          headerClass: "!bg-gray-200 justify-center",
          children: [
            {
              headerName: "Discount",
              field: "discount_pct",
              width: 75,
              headerClass: "!bg-gray-200",
              cellClass:
                "text-right !border-y-0 !border-l-0 !border-r !border-gray-300 bg-gray-200 after:content-['%']",
            },
            {
              headerName: "Adult Supp",
              field: "adult_supp_discount",
              width: 75,
              headerClass: "!bg-gray-200",
              cellClass:
                "text-right !border-y-0 !border-l-0 !border-r !border-gray-300 bg-gray-200",
              cellRenderer: CheckboxRenderer,
              cellRendererParams: { discount_type: "adult_supp" },
              editable: false,
            },
            {
              headerName: "Child Supp",
              field: "child_supp_discount",
              width: 75,
              headerClass: "!bg-gray-200",
              cellClass:
                "text-right !border-y-0 !border-l-0 !border-r !border-gray-300 bg-gray-200",
              cellRenderer: CheckboxRenderer,
              cellRendererParams: { discount_type: "child_supp" },
              suppressClickEdit: true,
            },
            {
              headerName: "Adult Meal",
              field: "adult_meal_discount",
              width: 70,
              headerClass: "!bg-gray-200",
              cellClass:
                "text-right !border-y-0 !border-l-0 !border-r !border-gray-300 bg-gray-200",
              cellRenderer: CheckboxRenderer,
              cellRendererParams: { discount_type: "adult_meal" },
            },
            {
              headerName: "Child Meal",
              field: "child_meal_discount",
              width: 70,
              headerClass: "!bg-gray-200",
              cellClass:
                "text-right !border-y-0 !border-l-0 !border-r !border-gray-300 bg-gray-200",
              cellRenderer: CheckboxRenderer,
              cellRendererParams: { discount_type: "child_meal" },
            },
            {
              headerName: "Peak Supp",
              field: "peak_supp_discount",
              width: 70,
              headerClass: "!bg-gray-200",
              cellClass:
                "text-right !border-y-0 !border-l-0 !border-r !border-gray-300 bg-gray-200",
              cellRenderer: CheckboxRenderer,
              cellRendererParams: { discount_type: "peak_supp" },
            },
            {
              headerName: "Extras",
              field: "extras_discount",
              width: 70,
              headerClass: "!bg-gray-200",
              cellClass:
                "text-right !border-y-0 !border-l-0 !border-r !border-gray-300 bg-gray-200",
              cellRenderer: CheckboxRenderer,
              cellRendererParams: { discount_type: "extras" },
            },
          ],
        },
        {
          field: "total",
          width: 70,
          type: "numberColumn",
          cellClass:
            "text-right !border-y-0 !border-l-0 !border-r !border-gray-200 font-bold",
        },
        {
          headerName: "Markup",
          field: "mark_up",
          width: 70,
          type: "numberColumn",
          cellClass:
            "text-right !border-y-0 !border-l-0 !border-r !border-gray-200",
        },
        {
          headerName: "PurchaseID",
          field: "gwg_purchase_id",
          cellClass:
            "text-right !border-y-0 !border-l-0 !border-r !border-gray-200",
          width: 80,
        },
        {
          headerName: "PurchaseCode",
          field: "gwg_purchase_code",
          cellClass: "!border-y-0 !border-l-0 !border-r !border-gray-200",
          flex: 1,
        },
        {
          headerName: "SalesID",
          field: "gwg_sales_id",
          cellClass:
            "text-right !border-y-0 !border-l-0 !border-r !border-gray-200",
          width: 80,
        },
        {
          headerName: "SalesCode",
          field: "gwg_sales_code",
          cellClass: "!border-y-0 !border-l-0 !border-r !border-gray-200",
          flex: 1,
        },
      ],
      defaultColDef: {
        editable: true,
        filter: false,
        sort: false,
        suppressMenu: true,
        suppressMovable: true,
        wrapHeaderText: true,
      },
    },
  },
};

document.addEventListener("DOMContentLoaded", () => {
  const RESERV_GRID_DIV = document.querySelector("#reserv-grid");
  new agGrid.Grid(RESERV_GRID_DIV, RESERV_GRID_OPTS);

  ["status", "hotel", "operator"].forEach((element) => {
    switch (element) {
      case "status":
        ajax("/api/" + element).then((response) => {
          loadRefData(0, response.data);
        });
        break;
      case "operator":
        ajax("/api/" + element).then((response) => {
          loadRefData(5, response.data);
        });
        break;
      case "hotel":
        ajax("/api/" + element).then((response) => {
          loadRefData(6, response.data);
        });
        break;
    }
  });

  const dataSource = {
    getRows: (params) => {
      ajax("/api/booking", params.request)
        .then((response) => {
          params.successCallback(response.data, response.total_rows);
        })
        .catch((e) => {
          console.error(e);
          params.failCallback();
        });
    },
  };

  RESERV_GRID_OPTS.api.setServerSideDatasource(dataSource);
});
