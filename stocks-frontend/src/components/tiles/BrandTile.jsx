import { nameMap } from "../../my-utils/nameRemapper";
import React from "react";
import { nanoid } from "nanoid";
import { AxiosHeaders as col } from "axios";
const iconApiURL = process.env.REACT_APP_ICON_API_URL || "";

export default function BrandTile(props) {
  const { titlePosition, brandName } = props;
  const spanDisplay = titlePosition === "right" ? "" : "block";
  const instanceId = nanoid();
  return (
    <figure
      key={`${instanceId}`}
      className={"item-center flex gap-3"}
    >
      <img
        alt={"brand logo"}
        className="flex h-8 w-8"
        src={iconApiURL.replace("%searchable%", nameMap(brandName))}
      />
      <span className={"font-bold capitalize " + spanDisplay}>{brandName}</span>
    </figure>
  );
}