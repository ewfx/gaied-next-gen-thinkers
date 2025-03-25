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
  