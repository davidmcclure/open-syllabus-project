

import _ from 'lodash';
import React, { Component } from 'react';
import classNames from 'classnames';


export default class extends Component {


  /**
   * Render the "cube grid" spinner.
   */
  render() {

    let cubes = _.range(9).map(function(i) {
      let cx = classNames('sk-cube', `sk-cube${i+1}`);
      return <div key={i} className={cx}></div>;
    });

    return (
      <div className="sk-cube-grid">
        {cubes}
      </div>
    );

  }


}
