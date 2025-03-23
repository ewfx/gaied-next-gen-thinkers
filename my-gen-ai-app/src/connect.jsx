import React, { useEffect, useState } from "react";
import Button from "@mui/material/Button";
import EnhancedTable from "./table";
import { createData, getMaxConfidaentObject, getRequestTypesCount } from "./utils/utils";
import { useContext } from "react";
import { MyContext } from "./app-route";
import BadgeComp from "./BadgeComp";
import Badge from "@mui/material/Badge";
import Stack from "@mui/material/Stack";
import MailIcon from "@mui/icons-material/Mail";

const WebSocketComponent = () => {
  const [data, setData] = useState([{}]);
  const [row, setRow] = useState([{}]);
  const [rowData, setRowData] = useState([{}]);
  const [headCells, setHeadCells] = useState([{}]);
  const [typeCount, setTypeCount] = useState({});
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
          const maxConfidenceObject = getMaxConfidaentObject(element);
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
        setTypeCount(getRequestTypesCount(rows));
        console.log("Rows details:", getRequestTypesCount(rows));
        setRow([...rows]);
        setRowData( [...rows]);
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
      socket.send("Hello from client");
    };

    socket.onmessage = (event) => {
      console.log("Received from server:", event.data);
      setData((prevData) => [JSON.parse(event.data), ...prevData]);
    };

    return () => {
      socket.close();
    };
  }, []);

  const getColor = (key,colors) => {
    //const colors = ["primary", "secondary", "success", "error", "warning", "info"];
    const index = Object.keys(typeCount).indexOf(key) % colors.length;
    return colors[index];
  };

  const TypeColors = [
    "#FF5733", // Red-Orange
    "#33FF57", // Green
    "#3357FF", // Blue
    "#FF33A8", // Pink
    "#A833FF", // Purple
    "#33FFF5", // Cyan
    "#FFD700", // Gold
    "#FF8C00", // Dark Orange
    "#8B0000", // Dark Red
    "#228B22"  // Forest Green
];
const Badgecolors = ["primary", "secondary", "success", "error", "warning", "info"];

const handleClick = (text) => {
  console.log("clicked", text);
  if(text==='All Types'){
    setRow([...rowData])
    return
  }
  const filteredData= rowData.filter(item => item.type === text);
  setRow(filteredData);
   
}
  return (
    <div>
       <h1>Email Classification</h1>
  <div className="badgeDetails">
      {Object.keys(typeCount).map((key, index) => (
          <Badge badgeContent={typeCount[key]} color={getColor(key,Badgecolors)} key={index}>
            <BadgeComp handleClick={handleClick} text={key} color={getColor(key,TypeColors)} />
          </Badge>
        ))}
            <Badge badgeContent={Object.keys(typeCount).length+1} color={'primary'}>
            <BadgeComp handleClick={handleClick} text={'All Types'} color={'#FF5733'} />
          </Badge>
        </div>
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
