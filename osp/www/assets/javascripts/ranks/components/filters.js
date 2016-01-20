

import _ from 'lodash';
import React, { Component } from 'react';
import { connect } from 'react-redux';

import FilterSelect from './filter-select';
import * as facets from './facets.yml';


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
          options={filterFields()}
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
          options={filterCountries()}
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


/**
 * Filter out blacklisted fields.
 *
 * @return {Object}
 */
function filterFields() {
  return _.reject(OSP.facets.field, function(f) {
    return _.includes(facets.field_blacklist, f.label);
  });
}


/**
 * Filter out non-whitelisted countries.
 *
 * @return {Object}
 */
function filterCountries() {
  return _.filter(OSP.facets.country, function(c) {
    return _.includes(facets.country_whitelist, c.label);
  });
}
