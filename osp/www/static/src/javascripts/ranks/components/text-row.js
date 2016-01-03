

import React, { Component, PropTypes } from 'react';

import Hit from './hit';


export default class extends Component {


  static propTypes = {
    hit: PropTypes.object.isRequired,
    rank: PropTypes.number.isRequired,
  }


  /**
   * Render a text row.
   */
  render() {

    let hit = new Hit(this.props.hit);

    return (
      <tr className="text-row">

        <td className="rank">
          {this.props.rank}
        </td>

        <td className="count">
          {hit.count()}
        </td>

        <td className="text">

          <div className="title" dangerouslySetInnerHTML={{
            __html: hit.field('title')
          }}></div>

          <div className="authors" dangerouslySetInnerHTML={{
            __html: hit.field('authors')
          }}></div>

          <div className="journal" dangerouslySetInnerHTML={{
            __html: hit.field('journal')
          }}></div>

          <div className="publisher" dangerouslySetInnerHTML={{
            __html: hit.field('publisher')
          }}></div>

        </td>

      </tr>
    );

  }


}
