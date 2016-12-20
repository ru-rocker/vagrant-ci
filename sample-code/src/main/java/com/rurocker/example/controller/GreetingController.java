package com.rurocker.example.controller;

import java.util.Date;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.rurocker.example.vo.Greeting;

/**
 * Rest Controller class for gretting api
 * 
 * @author ru-rocker
 *
 */
@RestController
@RequestMapping("/api")
public class GreetingController {

	private static final String template = "Howdy, %s";

	@RequestMapping("/greeting")
	public Greeting greeting(@RequestParam(value = "name", defaultValue = "World") String name) {
		return new Greeting(new Date(), String.format(template, name));
	}
}
