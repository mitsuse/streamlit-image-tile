import {
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { CSSProperties, ReactNode } from "react"
import "./image_tile.css"

interface State {}

class CaptionedImage extends StreamlitComponentBase<State> {
  public state: State = {}

  public render = (): ReactNode => {
    const image = this.props.args["image"]
    const height = this.props.args["height"]
    const width = this.props.args["width"]
    const right = this.props.args["right"]
    const caption = this.props.args["caption"]

    const styleOfRootContainer = {
        backgroundColor: "transparent",
    }

    const styleOfImageContainer = {
      display: "flex",
      justifyContent: "center",
    }

    const styleOfImage = {
      width: width,
      height: height,
    }

    const styleOfCaption: CSSProperties = {
      color: "#666666",
      fontFamily: "'IBM Plex Mono', monospace",
      fontSize: "0.7rem",
      textAlign: "center",
      marginTop: "4px",
      marginBottom: "4px",
      height: "50px",
    }

    const imageComponent = right ? (
      <a href={right.origin} rel="noreferrer" target="_blank">
        <img src={image} style={styleOfImage} />
      </a>
    ) : (
      <img src={image} style={styleOfImage} />
    )

    const captionComponent = right ? (
      <p style={styleOfCaption}>
        <a href={right.creator.url} rel="noreferrer" target="_blank">
          {right.creator.name}
        </a>{" "}
        on{" "}
        <a href={right.publisher.url} rel="noreferrer" target="_blank">
          {right.publisher.name}
        </a>
        . {caption}
      </p>
    ) : (
      <p style={styleOfCaption}>{caption}</p>
    )

    return (
      <div style={styleOfRootContainer}>
        <div style={styleOfImageContainer}>
            {imageComponent}
        </div>
        {captionComponent}
      </div>
    )
  }
}

export default withStreamlitConnection(CaptionedImage)
