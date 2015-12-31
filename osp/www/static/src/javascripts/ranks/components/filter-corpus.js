

import React, { Component } from 'react';
import Select from 'react-select';


export default class extends Component {


  /**
   * Render the corpus facets.
   */
  render() {
    return (
      <Select
        placeholder="Select corpora"
        options={OSP.facets.corpus}
      />
    );
  }


}
