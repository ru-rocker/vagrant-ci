package com.rurocker.example.test.vo;

import java.util.Date;

import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import com.rurocker.example.vo.Greeting;

@RunWith(SpringJUnit4ClassRunner.class)
public class GreetingVOTest {

	@Test
	public void testGreetingSetterGetter(){
		Date d = new Date();
		String content = "Lucas";
		Greeting greeting = new Greeting(d, content);
		Assert.assertEquals(d, greeting.getDate());
		Assert.assertEquals(content, greeting.getContent());
	}
}
