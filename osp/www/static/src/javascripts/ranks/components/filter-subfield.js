

import React, { Component } from 'react';
import Select from 'react-select';


export default class extends Component {


  /**
   * Render the subfield facets.
   */
  render() {
    return (
      <Select
        placeholder="All subfields"
        options={OSP.facets.subfield}
      />
    );
  }


}
