import React, { useState, createContext } from "react";
import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import CardMedia from "@mui/material/CardMedia";
import { CardActionArea } from "@mui/material";

import { AWS_S3_BASE_URL } from "../../../../constants";


export default function ProductCard({ product }: any) {
  const imageUrl = product?.image_url
    ? product.image_url.startsWith("http")
      ? product.image_url
      : (AWS_S3_BASE_URL || "") + product.image_url
    : "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500";

  return (
    <Card
      variant="outlined"
      sx={{ maxWidth: 300, width: "100%", flex: "1 0 20%" }}
    >
      <CardActionArea href={`/products/${product.slug}`}>
        <CardMedia
          sx={{ height: 200, objectFit: "cover" }}
          image={imageUrl}
          title={product.product_name}
        />
        <CardContent>
          <Typography variant="h5" fontSize={20} component="div">
            {product.product_name}
          </Typography>
          <Typography sx={{ mb: 1.5 }} color="text.secondary">
            {product.blurb}
          </Typography>
          <Typography variant="h5" fontSize={16} component="div">
            {product.sale_price ? <s>${product.price}</s> : `$${product.price}`}
          </Typography>
          {product.sale_price && (
            <Typography variant="h5" fontSize={16} color="red" component="div">
              {" "}
              SALE ${product.sale_price}
            </Typography>
          )}
        </CardContent>
      </CardActionArea>
    </Card>
  );
}
