

import _ from 'lodash';
import React, { Component } from 'react';
import classNames from 'classnames';


export default class extends Component {


  /**
   * Render the "cube grid" spinner.
   */
  render() {

    let circles = _.range(12).map(function(i) {
      let cx = classNames('sk-child', `sk-circle${i+1}`);
      return <div key={i} className={cx}></div>;
    });

    return (
      <div className="sk-circle">
        {circles}
      </div>
    );

  }


}
