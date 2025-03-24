import React from 'react';

const BadgeComp = ({ text, color,handleClick,selected }) => {
    const badgeStyle = {
        backgroundColor: color,
        padding: '10px',
         borderRadius: '20px',
        color: !selected?'black':'white',
        display: 'inline-block',
        cursor: 'pointer',
        fontWeight: 'bold'
    };

    return <span onClick={()=>handleClick(text)} style={badgeStyle}>{text}</span>;
};

export default BadgeComp;