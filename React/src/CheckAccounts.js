import axios from "axios";
import React, { useEffect, useState } from "react";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import Switch from "@material-ui/core/Switch";
import { Button } from "@material-ui/core";
import PublishIcon from "@material-ui/icons/Publish";
import { ListTargets } from "./TargetsList";
import { DeleteButton } from "./DeleteButton";
import { EditAccounts } from "./EditAccounts";


export const CheckAccounts = () => {
  const [accounts, setAccounts] = useState([]);
  const fetchAccounts = async () => {
    const res = await axios.get(`${process.env.REACT_APP_URL}/ListAccounts`);
    setAccounts(res.data);
  };
  const [targets, setTargets] = useState([]);
  const fetchTargets = async () => {
    const TargetList = await axios.get(
      `${process.env.REACT_APP_URL}/Targets`
    );
    setTargets(TargetList.data);
  };
  useEffect(() => {
    fetchAccounts();
    fetchTargets();
  }, []);
  const ListRendered = accounts.map(({ _id, username, password, target, dm_text, dm_link }) => (
    <ListItem key={_id}>
      <ListItemText style={{ marginRight: "23%" }} primary={username} secondary={`The target is ${target}`} />
      <ListTargets username={username} targets={targets}  />

      <DeleteButton username={username} />

      <EditAccounts dm_text={dm_text} dm_link={dm_link} username={username}/>
    </ListItem>
  ));

  return <>{ListRendered}</>;
};
