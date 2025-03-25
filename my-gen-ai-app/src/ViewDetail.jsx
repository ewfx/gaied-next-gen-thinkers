import React, { useEffect, useState } from "react";
import { useLocation, useParams, useNavigate } from "react-router-dom";
import EnhancedTable from "./table";
import { useContext } from "react";
import { MyContext } from "./app-route";
import Button from "@mui/material/Button";
import { convertLabelToTitleCase } from "./utils/utils";

const ViewDetail = () => {
  const [row, setRow] = useState([]);
  const [headCells, setHeadCells] = useState([]);
  const [key, setKey] = useState([]);
  const [otherInfo, setOtherInfo] = useState({});
  const [filteredItem, setFilteredItem] = useState({});
  const navigate = useNavigate();

  const { id } = useParams();
  const contextValue = useContext(MyContext);
  console.log("Context Value:", contextValue);

  useEffect(() => {
    if (contextValue?.contextData) {
      const rows = [];
      let headCellsTemp = [];
      const filteredData = contextValue?.contextData?.filter(
        (element) => element.id == id
      );
      console.log("Filtered Data:", filteredData);
      setFilteredItem(filteredData[0]);
      const otherInfo = filteredData[0]?.additional_fields;
      Object.keys(otherInfo).forEach((key) => {
        console.log("Key:", key);
        if (otherInfo[key] === "Not Found") {
          delete otherInfo[key];
        }
      });
      setOtherInfo(otherInfo);

      if (filteredData && filteredData.length > 0) {
        filteredData[0]?.classifications?.forEach((element, id) => {
            rows.push({ ...element, id: Math.random().toString(36).substr(2, 9) });
        });
        const keys = Object.keys(filteredData[0]?.classifications[0]);
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
        setRow(rows);
        setHeadCells(headCellsTemp);
      }
    } else {
      navigate("/");
    }
  }, [contextValue, id]);

  return (
    <div
      style={{
        display: "flex",
        height: "100vh",
        flexDirection: "column",
        rowGap: "30px",
      }}
    >
      <h1>{filteredItem?.email_subject}</h1>
      <EnhancedTable
        source={"details"}
        keyData={key}
        rowTableData={row}
        headCellsData={headCells}
      />
      {otherInfo && Object.keys(otherInfo).length > 0 ? (
        <>
         <h1>Other Important Details</h1>
          <table style={{ width: "50vw",textAlign: "justify",alignSelf: "anchor-center" }}>
            <tbody>
              {Object.keys(otherInfo || {}).map((key) => (
                <tr key={key} style={{ border: "1px solid black" }}>
                  <td style={{ padding: "5px", border: "1px solid black" }}>
                    <strong>{key}:</strong>
                  </td>
                  <td style={{ padding: "5px", border: "1px solid black" }}>
                    {typeof otherInfo[key] === "object"
                      ? JSON.stringify(otherInfo[key])
                      : otherInfo[key]}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      ) : (
        <p>No details available</p>
      )}
      <div style={{ display: "flex", gap: "10px", justifyContent: "center" }}>
        <Button variant="outlined" onClick={() => navigate("/")}>
          Go Back
        </Button>
        <Button variant="contained" onClick={() => console.log("Assign")}>
          Assign
        </Button>
      </div>
    </div>
  );
};

export default ViewDetail;
