export function createData(obj) {
    return {
      ...obj
    };
  }

  export const getMaxConfidaentObject = (element) => {
    return element?.classifications.reduce(
      (max, obj) => {
        return parseFloat(obj.confidence_score) >
          parseFloat(max.confidence_score)
          ? obj
          : max;
      },
      element.classifications[0]
    );
  }


  export const getRequestTypesCount = (data) => {
   const item= data.reduce((acc, obj) => {
      acc[obj.request_type] = (acc[obj.request_type] || 0) + 1;
      return acc;
  }, {});
    return Object.entries(item).map(([request_type, value]) => ({
        type: request_type,
        value: value,
        selected: false
    }));
  }

  export const convertLabelToTitleCase = (key) => {
    return key
      .split('_')
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  export const  extractClassificationsDetails = (dataArray) => {
    let dropdownValues = {};
    if(dataArray?.length > 0){
      dataArray.forEach(email => {
        email.classifications.forEach(classification => {
            let requestType = classification.request_type;
            let subRequestTypes = classification.sub_request_type.map(sub => sub.sub_request_type);
  
            if (!dropdownValues[requestType]) {
                dropdownValues[requestType] = new Set();
            }
  
            subRequestTypes.forEach(subType => dropdownValues[requestType].add(subType));
        });
    });
  
    // Convert Set to Array
    Object.keys(dropdownValues).forEach(key => {
        dropdownValues[key] = Array.from(dropdownValues[key]);
    });
  
    return dropdownValues;
  }
  return []
}

export const getTopRequestTypes = (emails, topN = 3) => {
  const requestCount = {};

  emails.forEach(email => {
      // Find classification with highest confidence score
      const highestClassification = email.classifications.reduce((max, curr) =>
          curr.confidence_score > max.confidence_score ? curr : max, { confidence_score: -1 });

      if (highestClassification.confidence_score > 0 || highestClassification.confidence_score === 0) {
          const requestType = highestClassification.request_type;
          requestCount[requestType] = (requestCount[requestType] || 0) + 1;

          // Count sub-request types if available
          if (highestClassification.sub_request_type && highestClassification.sub_request_type.length > 0) {
              highestClassification.sub_request_type.forEach(subType => {
                  const subRequestType = `${requestType} - ${subType.sub_request_type}`;
                  requestCount[subRequestType] = (requestCount[subRequestType] || 0) + 1;
              });
          }
      }
  });

  // Sort by count (descending) and get top N request types
  return Object.entries(requestCount)
      .sort((a, b) => b[1] - a[1])
      .slice(0, topN)
      .reduce((acc, [key, value]) => ({ ...acc, [key]: value }), {}); // Convert back to object
};
  