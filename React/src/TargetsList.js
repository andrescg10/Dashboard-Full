import axios from "axios";
import React from "react";
import NativeSelect from "@material-ui/core/NativeSelect";

export const ListTargets = ({ username, targets}) => {
  const HandleChange = async (e) => {
    await axios.post(`${process.env.REACT_APP_URL}/UpdateTarget`, {
      username: username,
      target: e.target.value,
    });
  };
  const TargetsList = targets.map(({ _id, target }) => (
    <option key={_id} value={target}>
      {target}
    </option>
  ));

  return <NativeSelect onChange={HandleChange}>{TargetsList}</NativeSelect>;
};
