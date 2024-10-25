package com.han.youtube;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@SpringBootApplication(exclude = {DataSourceAutoConfiguration.class})
public class SeesoApplication {

	public static void main(String[] args) {
		SpringApplication.run(SeesoApplication.class, args);
	}

	@Configuration
	public class WebConfig implements WebMvcConfigurer {

		@Override
		public void addCorsMappings(CorsRegistry registry) {
			registry.addMapping("/api/**")
					.allowedOrigins("http://localhost:3000")  // React 앱이 실행되는 주소
					.allowedOrigins("http://localhost:9000")  // React 앱이 실행되는 주소
					.allowedOriginPatterns("*")
					.allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
					.allowedHeaders("*")
					.allowCredentials(true);
		}
		@Override
		public void addInterceptors(InterceptorRegistry registry) {
			registry.addInterceptor(new HandlerInterceptor() {
				@Override
				public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler,
									   ModelAndView modelAndView) throws Exception {
					// COEP 헤더 추가
					response.setHeader("Cross-Origin-Embedder-Policy", "unsafe-none");
					response.setHeader("Cross-Origin-Opener-Policy", "same-origin"); // COOP 헤더 추가, 필요 시
					response.setHeader("Cross-Origin-Resource-Policy", "cross-origin");
				}
			});
		}


	}

}
