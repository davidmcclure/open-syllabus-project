

import React, { Component, PropTypes } from 'react';

import Hit from './hit';
import Field from './field';


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
          {hit.count}
        </td>

        <td className="text">

          <div className="title" dangerouslySetInnerHTML={{
            __html: hit.field('title')
          }}></div>

          <Field label="authors" value={hit.field('authors')}/>
          <Field label="journal" value={hit.field('journal')}/>
          <Field label="publisher" value={hit.field('publisher')}/>

        </td>

      </tr>
    );

  }


}
