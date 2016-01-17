

import React, { Component } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

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
          filter="field_id"
          name="field"
          options={OSP.facets.field}
          value={this.props.filters.field_id}
          publish={this.props.changeFieldFilter}
        />

        <FilterSelect
          filter="institution_id"
          name="institution"
          options={OSP.facets.institution}
          value={this.props.filters.institution_id}
          publish={this.props.changeInstitutionFilter}
        />

        <FilterSelect
          filter="state"
          name="state"
          options={OSP.facets.state}
          value={this.props.filters.state}
          publish={this.props.changeStateFilter}
        />

        <FilterSelect
          filter="country"
          name="country"
          options={OSP.facets.country}
          value={this.props.filters.country}
          publish={this.props.changeCountryFilter}
        />

        <FilterSelect
          filter="corpus"
          name="corpus"
          options={OSP.facets.corpus}
          value={this.props.filters.corpus}
          publish={this.props.changeCorpusFilter}
        />

      </div>
    );
  }


}
