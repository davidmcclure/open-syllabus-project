

import _ from 'lodash';
import React, { Component, PropTypes } from 'react';

import HitCount from './hit-count';
import ClearFilters from './clear-filters';
import Search from './search';
import TextList from './text-list';


export default class extends Component {


  /**
   * Render the ranking results.
   */
  render() {
    return (
      <div id="results">

        <div className="list-header">
          <HitCount />
          <ClearFilters />
        </div>

        <Search />
        <TextList />

      </div>
    );
  }


}
