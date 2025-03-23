import React, { useEffect, useState } from "react";
import Button from "@mui/material/Button";
import EnhancedTable from "./table";
import { createData } from "./utils/utils";
import { useContext } from "react";
import { MyContext } from "./app-route";
import BadgeComp from "./BadgeComp";
import Badge from "@mui/material/Badge";
import Stack from "@mui/material/Stack";
import MailIcon from "@mui/icons-material/Mail";

const WebSocketComponent = () => {
  const [data, setData] = useState([{}]);
  const [row, setRow] = useState([{}]);
  const [headCells, setHeadCells] = useState([{}]);
  const [key, setKey] = useState([]);
  const { setContextData } = useContext(MyContext);

  useEffect(() => {
    fetch("http://localhost:3000/data")
      .then((response) => response.json())
      .then((serverData) => {
        console.log("Data from server:", serverData);
        setContextData(serverData);
        const rows = [];
        let headCellsTemp = [];
        serverData?.forEach((element) => {
          const maxConfidenceObject = element?.request_types.reduce(
            (max, obj) => {
              return parseFloat(obj.confidence_score) >
                parseFloat(max.confidence_score)
                ? obj
                : max;
            },
            element.request_types[0]
          );
          console.log("Object with max confidence_score:", maxConfidenceObject);
          rows.push({ ...maxConfidenceObject, id: element.id });
          const keys = Object.keys(maxConfidenceObject);
          setKey(keys);
          console.log("Keys:", keys);
          headCellsTemp = [];
          keys.forEach((key) => {
            headCellsTemp.push({
              id: key,
              numeric: false,
              disablePadding: true,
              label: key,
            });
          });
        });
        setRow((prevRow) => [...rows]);
        setHeadCells((prevHeadCells) => [
          ...headCellsTemp,
          {
            id: "action",
            numeric: false,
            disablePadding: true,
            label: "Action",
          },
        ]);
      })
      .catch((error) => console.error("Error fetching data:", error));

    const socket = new WebSocket("ws://localhost:8765");

    socket.onopen = () => {
      console.log("Connected to WebSocket server");
      socket.send("Hello from client!");
    };

    socket.onmessage = (event) => {
      console.log("Received from server:", event.data);
      setData((prevData) => [JSON.parse(event.data), ...prevData]);
    };

    return () => {
      socket.close();
    };
  }, []);

  return (
    <div>
      <div className="badgeDetails">
        <Badge badgeContent={4} color="success">
          <BadgeComp text={"Finance"} color={"black"} />
        </Badge>
        <Badge badgeContent={4} color="primary">
          <BadgeComp text={"Adjustment"} color={"gray"} />
        </Badge>
        <Badge badgeContent={4} color="secondary">
          <BadgeComp text={"Vacation"} color={"blue"} />
        </Badge>
      </div>

      <h1>Email Classification</h1>
      <EnhancedTable
        keyData={key}
        data={data}
        rowTableData={row}
        headCellsData={headCells}
      />
    </div>
  );
};

export default WebSocketComponent;
