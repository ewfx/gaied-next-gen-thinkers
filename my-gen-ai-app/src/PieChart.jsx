import * as React from 'react';
import { PieChart } from '@mui/x-charts/PieChart';

export default function BasicPie({ typeCount,handleClick }) {
   const [dataSet,setDataSet]= React.useState([]);
    React.useEffect(() => {
        const transformedData = typeCount.map((item, index) => ({
            id: index,
            value: item.value,
            label: item.type
        }));
        setDataSet(transformedData);
    }, [typeCount]);

    const handleClickEvent = (d) => {
        const selectedKey = typeCount[d.dataIndex].type;
        handleClick(selectedKey);
    }
  return (
    <PieChart
    onItemClick={(event, d) => handleClickEvent(d)}
      series={[
        {
          data:dataSet,
        },
      ]}
      width={400}
      height={200}
    />
  );
}