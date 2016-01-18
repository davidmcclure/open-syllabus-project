

import React, { Component } from 'react';
import { connect } from 'react-redux';

import FilterSelect from './filter-select';


@connect(
  state => ({
    filters: state.filters
  }),
)
export default class extends Component {


  /**
   * Render the filter widgets.
   */
  render() {
    return (
      <div id="filters">

        <FilterSelect
          filter="field_id"
          name="field"
          options={OSP.facets.field}
          value={this.props.filters.field_id}
        />

        <FilterSelect
          filter="institution_id"
          name="institution"
          options={OSP.facets.institution}
          value={this.props.filters.institution_id}
        />

        <FilterSelect
          filter="state"
          name="state"
          options={OSP.facets.state}
          value={this.props.filters.state}
        />

        <FilterSelect
          filter="country"
          name="country"
          options={OSP.facets.country}
          value={this.props.filters.country}
        />

        <FilterSelect
          filter="corpus"
          name="corpus"
          options={OSP.facets.corpus}
          value={this.props.filters.corpus}
        />

      </div>
    );
  }


}
