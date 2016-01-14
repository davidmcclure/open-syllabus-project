

import React, { Component, PropTypes } from 'react';


export default class extends Component {


  static propTypes = {
    label: PropTypes.string.isRequired,
  };


  /**
   * Render a metadata field.
   */
  render() {

    if (!this.props.value) {
      return null;
    }

    else return (
      <div className="field">

        <span className="value" dangerouslySetInnerHTML={{
          __html: this.props.value
        }}></span>

      </div>
    );

  }


}
