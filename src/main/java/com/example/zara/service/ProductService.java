package com.example.zara.service;

import org.springframework.stereotype.Service;

import com.example.zara.domain.Product;
import com.example.zara.repository.ProductRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class ProductService {

    private final ProductRepository productRepository;

    public Product getProduct(Long id) {
        return productRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("상품 없음"));
    }
    
}
