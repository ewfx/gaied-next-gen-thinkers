export function createData(obj) {
    return {
      ...obj
    };
  }

  export const getMaxConfidaentObject = (element) => {
    return element?.request_types.reduce(
      (max, obj) => {
        return parseFloat(obj.confidence_score) >
          parseFloat(max.confidence_score)
          ? obj
          : max;
      },
      element.request_types[0]
    );
  }


  export const getRequestTypesCount = (data) => {
    return data.reduce((acc, obj) => {
      acc[obj.type] = (acc[obj.type] || 0) + 1;
      return acc;
  }, {});
  }
