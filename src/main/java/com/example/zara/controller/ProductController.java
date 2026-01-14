package com.example.zara.controller;

import org.springframework.data.domain.Page;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.example.zara.domain.Product;
import com.example.zara.dto.ProductListResponse;
import com.example.zara.dto.ProductResponse;
import com.example.zara.service.ProductService;

import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/api/products")
@RequiredArgsConstructor
public class ProductController {

    private final ProductService productService;

    @GetMapping
    public Page<ProductListResponse> getProducts(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size
    ) {
        return productService.getProducts(page, size)
                .map(p -> new ProductListResponse(
                        p.getId(),
                        p.getName(),
                        p.getPrice(),
                        p.getPriceText()
                ));
    }

    @GetMapping("/{id}")
    public ProductResponse getProduct(@PathVariable Long id) {
        Product p = productService.getProduct(id);

        return new ProductResponse(
                p.getId(),
                p.getName(),
                p.getPrice(),
                p.getPriceText()
        );
    }
    
}
