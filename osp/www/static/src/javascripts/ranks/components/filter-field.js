

import React, { Component } from 'react';
import Select from 'react-select';


export default class extends Component {


  /**
   * Render the field facets.
   */
  render() {
    return (
      <Select
        placeholder="All fields"
        options={OSP.facets.field}
      />
    );
  }


}
