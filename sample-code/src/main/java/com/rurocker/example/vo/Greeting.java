package com.rurocker.example.vo;

import java.util.Date;

import com.fasterxml.jackson.annotation.JsonFormat;

/**
 * Value object class for JSON
 * 
 * @author ru-rocker
 *
 */
public class Greeting {

	@JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd HH:mm:ss", locale = "ID", timezone = "GMT+7")
	private Date date;
	private String content;

	public Greeting(Date date, String content) {
		this.date = date;
		this.content = content;
	}

	public Date getDate() {
		return (Date) date.clone();
	}

	public void setDate(Date date) {
		this.date = date;
	}

	public String getContent() {
		return content;
	}

	public void setContent(String content) {
		this.content = content;
	}

}
