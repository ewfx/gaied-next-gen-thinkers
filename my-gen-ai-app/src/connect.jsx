import React, { useEffect, useState } from "react";
import EnhancedTable from "./table";
import { convertLabelToTitleCase, getMaxConfidaentObject, getRequestTypesCount } from "./utils/utils";
import { useContext } from "react";
import { MyContext } from "./app-route";
import BadgeComp from "./BadgeComp";
import Badge from "@mui/material/Badge";
import BasicPie from "./PieChart";
import ControlledSwitches from "./swich";
let pData = [];
const WebSocketComponent = () => {
  const [data, setData] = useState([{}]);
  const [payloadData, setPayloadData] = useState([]);
  const [row, setRow] = useState([{}]);
  const [rowData, setRowData] = useState([{}]);
  const [headCells, setHeadCells] = useState([{}]);
  const [typeCount, setTypeCount] = useState([{}]);
  const [key, setKey] = useState([]);
  const [allTypeSelected, setAllTypeSelected] = useState(true);
  const { contextData, setContextData } = useContext(MyContext);
  const [showGraph, setShowGraph] = useState(false);

const formatData=(serverData)=>{
  console.log("Data from server:", serverData);
        // setContextData({serverData, typeCount});
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
              label: convertLabelToTitleCase(key),
            });
          });
        });
        setTypeCount(getRequestTypesCount(rows));
        console.log("Rows details:", getRequestTypesCount(rows));
        setRow([...rows]);
        setRowData([...rows]);
        setHeadCells((prevHeadCells) => [
          ...headCellsTemp,
          {
            id: "Action",
            numeric: false,
            disablePadding: true,
            label: "Action",
          },
        ]);
}

  useEffect(() => {
    formatData(contextData?.payload);
  }, []);

  const getColor = (key, colors) => {
    const index =
      typeCount.findIndex((item) => item.type === key) % colors.length;
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
    "#228B22", // Forest Green
  ];
  const Badgecolors = [
    "primary",
    "secondary",
    "success",
    "error",
    "warning",
    "info",
  ];

  const handleClick = (text) => {
    console.log("clicked", text);
    const updatedTypeCount = typeCount.map((item) =>
      item.type === text
        ? { ...item, selected: true }
        : { ...item, selected: false }
    );
    setTypeCount(updatedTypeCount);
    setAllTypeSelected(false);
    if (text === "All Types") {
      setAllTypeSelected(true);
      setRow([...rowData]);
      return;
    }
    const filteredData = rowData.filter((item) => item.request_type === text);
    setRow(filteredData);
  };

  const handleLableChange = (value) => {
    console.log("handleLableChange", value);
    const updatedTypeCount = typeCount.map((item) => ({
      ...item,
      selected: false,
    }));
    setAllTypeSelected(true);
    setTypeCount(updatedTypeCount);
    setShowGraph(value);
    setRow([...rowData]);
  };
  return (
    <div>
      <h1>Request Types</h1>
      <ControlledSwitches
        setShowGraph={setShowGraph}
        handleLableChange={handleLableChange}
      />
      <div className="badgeDetails">
        {!showGraph && (
          <div className="badges">
            {typeCount.map((item, index) => (
              <Badge
                badgeContent={item.value}
                color={getColor(item.type, Badgecolors)}
                key={index}
              >
                <BadgeComp
                  handleClick={handleClick}
                  text={item.type}
                  color={item.selected ? "#4CAF50" : "white"}
                  selected={item.selected}
                />
              </Badge>
            ))}
            <Badge
              badgeContent={Object.keys(typeCount).length + 1}
              color={"primary"}
            >
              <BadgeComp
                handleClick={handleClick}
                text={"All Types"}
                color={allTypeSelected ? "#4CAF50" : "white"}
                selected={allTypeSelected}
              />
            </Badge>
            <div />
          </div>
        )}
        {showGraph && (
          <BasicPie typeCount={typeCount} handleClick={handleClick} />
        )}
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
