

import React, { Component } from 'react';
import { connect } from 'react-redux';

import * as actions from '../actions/filters';
import FilterSelect from './filter-select';


@connect(
  state => ({
    filters: state.filters
  }),
  actions,
)
export default class extends Component {


  /**
   * Render the filter widgets.
   */
  render() {
    return (
      <div id="filters">

        <FilterSelect
          options={OSP.facets.corpus}
          value={this.props.filters.corpus}
          placeholder="All corpora"
          publish={this.props.changeCorpusFilter}
        />

        <FilterSelect
          options={OSP.facets.field}
          value={this.props.filters.field_id}
          placeholder="All fields"
          publish={this.props.changeFieldFilter}
        />

        <FilterSelect
          options={OSP.facets.subfield}
          value={this.props.filters.subfield_id}
          placeholder="All subfields"
          publish={this.props.changeSubfieldFilter}
        />

        <FilterSelect
          options={OSP.facets.institution}
          value={this.props.filters.institution_id}
          placeholder="All institutions"
          publish={this.props.changeInstitutionFilter}
        />

        <FilterSelect
          options={OSP.facets.state}
          value={this.props.filters.state}
          placeholder="All states"
          publish={this.props.changeStateFilter}
        />

        <FilterSelect
          options={OSP.facets.country}
          value={this.props.filters.country}
          placeholder="All countries"
          publish={this.props.changeCountryFilter}
        />

      </div>
    );
  }


}
