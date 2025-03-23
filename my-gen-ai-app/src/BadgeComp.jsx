import React from 'react';

const BadgeComp = ({ text, color }) => {
    const badgeStyle = {
        backgroundColor: color,
        padding: '10px',
        borderRadius: '5px',
        color: 'white',
        display: 'inline-block'
    };

    return <span style={badgeStyle}>{text}</span>;
};

export default BadgeComp;