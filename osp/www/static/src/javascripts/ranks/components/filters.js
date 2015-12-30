

import React, { Component } from 'react';

import FilterCorpus from './filter-corpus';
import FilterField from './filter-field';
import FilterSubfield from './filter-subfield';
import FilterInstitution from './filter-institution';
import FilterState from './filter-state';
import FilterCountry from './filter-country';


export default class extends Component {


  /**
   * Render the filter widgets.
   */
  render() {
    return (
      <div id="filters">
        <FilterCorpus />
        <FilterField />
        <FilterSubfield />
        <FilterInstitution />
        <FilterState />
        <FilterCountry />
      </div>
    );
  }


}
