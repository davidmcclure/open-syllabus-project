

import React, { Component } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import * as filterActions from '../actions/filters';
import * as resultActions from '../actions/results';
import Search from './search';
import FilterSelect from './filter-select';


@connect(

  state => ({
    filters: state.filters
  }),

  dispatch => {
    return bindActionCreators({
      ...filterActions,
      ...resultActions,
    }, dispatch);
  }

)
export default class extends Component {


  /**
   * Query for initial results.
   */
  componentDidMount() {
    //this.props.loadResults(this.props.filters);
  }


  /**
   * Query for new results when filters change.
   */
  componentDidUpdate() {
    this.props.loadResults(this.props.filters);
  }


  /**
   * Render the filter widgets.
   */
  render() {
    return (
      <div id="filters">

        <Search />

        <FilterSelect
          name="corpus"
          options={OSP.facets.corpus}
          value={this.props.filters.corpus}
          publish={this.props.changeCorpusFilter}
        />

        <FilterSelect
          name="field"
          options={OSP.facets.field}
          value={this.props.filters.field_id}
          publish={this.props.changeFieldFilter}
        />

        <FilterSelect
          name="subfield"
          options={OSP.facets.subfield}
          value={this.props.filters.subfield_id}
          publish={this.props.changeSubfieldFilter}
        />

        <FilterSelect
          name="institution"
          options={OSP.facets.institution}
          value={this.props.filters.institution_id}
          publish={this.props.changeInstitutionFilter}
        />

        <FilterSelect
          name="state"
          options={OSP.facets.state}
          value={this.props.filters.state}
          publish={this.props.changeStateFilter}
        />

        <FilterSelect
          name="country"
          options={OSP.facets.country}
          value={this.props.filters.country}
          publish={this.props.changeCountryFilter}
        />

      </div>
    );
  }


}
