package com.rurocker.example.test.controller;

import static org.hamcrest.Matchers.is;
import static org.hamcrest.Matchers.notNullValue;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.test.web.servlet.setup.MockMvcBuilders.webAppContextSetup;

import java.nio.charset.Charset;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.MockitoAnnotations;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.converter.json.MappingJackson2HttpMessageConverter;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.test.context.web.WebAppConfiguration;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.web.context.WebApplicationContext;

import com.rurocker.example.controller.GreetingController;

@RunWith(SpringJUnit4ClassRunner.class)
@WebAppConfiguration
@ContextConfiguration(locations = { "classpath:/rest-servlet-test.xml" })
public class GreetingControllerTest {

	@Autowired
	private WebApplicationContext webApplicationContext;

	@Autowired
	private MappingJackson2HttpMessageConverter jacksonMessageConverter;

	private MediaType contentType = new MediaType(MediaType.APPLICATION_JSON.getType(),
			MediaType.APPLICATION_JSON.getSubtype(), Charset.forName("utf-8"));

	private MockMvc mockMvc;

	@InjectMocks
	private GreetingController greetingController;

	@Before
	public void setup() throws Exception {
		MockitoAnnotations.initMocks(this);
		this.mockMvc = webAppContextSetup(webApplicationContext).build();
		mockMvc = MockMvcBuilders.standaloneSetup(greetingController).setMessageConverters(jacksonMessageConverter)
				.build();
	}

	@Test
	public void testGreetingWithEmptyRequestParameterAndReturnWorldAsDefault() throws Exception {
		mockMvc.perform(get("/api/greeting").contentType(contentType))
			.andExpect(status().isOk())
			.andExpect(jsonPath("$.date", notNullValue()))
			.andExpect(jsonPath("$.content", is("Hello, World!")));
		
	}
	
	@Test
	public void testGreetingWithRequestParameterMezutAndReturnMezut() throws Exception {
		mockMvc.perform(get("/api/greeting?name=Mezut").contentType(contentType))
		.andExpect(status().isOk())
		.andExpect(jsonPath("$.date", notNullValue()))
		.andExpect(jsonPath("$.content", is("Hello, Mezut!")));
		
	}
}
