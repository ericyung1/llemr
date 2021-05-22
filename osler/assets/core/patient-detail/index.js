import "regenerator-runtime/runtime";

import React from "react";
import ReactDOM from "react-dom";
import PatientDetail from "./components/PatientDetail";

export function render(props) {
  ReactDOM.render(
    <PatientDetail {...props} />,
    document.getElementById("root")
  );
}
